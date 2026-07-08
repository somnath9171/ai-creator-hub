from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import redis.asyncio as aioredis
from src.database import engine, Base
from src.api.v1.auth_endpoints import auth_router
from src.api.v1.subscription_endpoints import sub_router

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app.state.redis = await aioredis.from_url("redis://redis:6379/0")
    yield
    await app.state.redis.close()

app = FastAPI(title="AI Creator Hub Normalized Engine Container", lifespan=app_lifespan)

app.include_router(auth_router, prefix="/api")
app.include_router(sub_router, prefix="/api")

@app.middleware("http")
async def attach_state_to_request_context(request: Request, call_next):
    request.state.redis = request.app.state.redis
    return await call_next(request)
