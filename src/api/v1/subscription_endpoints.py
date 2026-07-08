from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from src.database import get_db_session
from src.auth.jwt_handler import JWTManager
from src.services.toggle_registry import ToggleRegistryService

sub_router = APIRouter(prefix="/v1/subscription", tags=["Subscription & System Feature Registry"])

async def get_redis_client(request: Request) -> aioredis.Redis:
    return request.app.state.redis

@sub_router.get("/creator-dashboard")
async def access_creator_services_dashboard(
    db: AsyncSession = Depends(get_db_session),
    redis: aioredis.Redis = Depends(get_redis_client),
    token_data: dict = Depends(JWTManager.verify_token)
):
    """
    Protects Creator routes against global operational feature toggles natively.
    """
    is_active = await ToggleRegistryService.is_feature_active("creator_services", db, redis)
    if not is_active:
        raise HTTPException(status_code=403, detail="Creator Services are currently disabled via internal operations.")
        
    return {"status": "granted", "payload": "Welcome to Creator Hub Analytics Platform Matrix Engine."}
