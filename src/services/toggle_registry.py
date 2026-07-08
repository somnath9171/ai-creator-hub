import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import redis.asyncio as aioredis
from src.models.subscription_models import GlobalFeatureToggle

class ToggleRegistryService:
    @classmethod
    async def is_feature_active(cls, feature_key: str, db: AsyncSession, redis: aioredis.Redis) -> bool:
        """
        Calculates feature status dynamically via high-speed Redis lookup. Falls back to DB.
        """
        cache_key = f"toggle:{feature_key}"
        cached_val = await redis.get(cache_key)
        
        if cached_val is not None:
            return json.loads(cached_val)

        stmt = select(GlobalFeatureToggle).where(GlobalFeatureToggle.feature_key == feature_key)
        toggle = (await db.execute(stmt)).scalar_one_or_none()
        
        status = toggle.is_enabled if toggle else True
        await redis.setex(cache_key, 300, json.dumps(status))
        return status

    @classmethod
    async def set_feature_status(cls, feature_key: str, status: bool, db: AsyncSession, redis: aioredis.Redis):
        stmt = select(GlobalFeatureToggle).where(GlobalFeatureToggle.feature_key == feature_key)
        toggle = (await db.execute(stmt)).scalar_one_or_none()

        if not toggle:
            toggle = GlobalFeatureToggle(feature_key=feature_key, is_enabled=status)
            db.add(toggle)
        else:
            toggle.is_enabled = status
            
        await db.commit()
        await redis.set(f"toggle:{feature_key}", json.dumps(status))
