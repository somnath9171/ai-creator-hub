from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from src.database import get_db_session
from src.auth.telegram_auth import TelegramAuthValidator
from src.auth.jwt_handler import JWTManager
from src.models.subscription_models import PlatformUser, UserEntitlement, PlanType

auth_router = APIRouter(prefix="/v1/auth", tags=["Telegram Core Authentication"])

@auth_router.post("/telegram-login")
async def process_telegram_widget_auth(
    init_data: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db_session)
):
    validated_payload = TelegramAuthValidator.validate_init_data(init_data)
    user_payload = json.loads(validated_payload.get("user", "{}"))
    tg_id = user_payload.get("id")
    
    if not tg_id:
        raise HTTPException(status_code=400, detail="Payload context missing identifying fields.")

    user = (await db.execute(select(PlatformUser).where(PlatformUser.telegram_id == tg_id))).scalar_one_or_none()

    if not user:
        user = PlatformUser(
            telegram_id=tg_id,
            username=user_payload.get("username"),
            first_name=user_payload.get("first_name", "Telegram User"),
            last_name=user_payload.get("last_name")
        )
        db.add(user)
        db.add(UserEntitlement(telegram_id=tg_id, active_plan=PlanType.FREE))
        await db.commit()
    elif user.is_suspended:
        raise HTTPException(status_code=403, detail="Account administratively locked.")

    token = JWTManager.create_access_token(telegram_id=user.telegram_id, role="USER")
    return {"access_token": token, "token_type": "bearer"}
