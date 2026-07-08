import enum
from datetime import datetime, timezone
from sqlalchemy import String, BigInteger, Numeric, Enum, DateTime, JSON, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

class PlanType(str, enum.Enum):
    FREE = "FREE"
    BASIC = "BASIC"
    PRO = "PRO"
    BUSINESS = "BUSINESS"
    CREATOR = "CREATOR"

class FeatureKey(str, enum.Enum):
    UPSCALER_4K = "UPSCALER_4K"
    UPSCALER_8K = "UPSCALER_8K"
    UPSCALER_16K = "UPSCALER_16K"
    BATCH_PROCESSING = "BATCH_PROCESSING"
    BG_REMOVER = "BG_REMOVER"
    ADVANCED_OCR = "ADVANCED_OCR"
    AI_CODE_GEN = "AI_CODE_GEN"
    TG_FORWARDER = "TG_FORWARDER"
    CREATOR_SERVICES = "CREATOR_SERVICES"

class PlatformUser(Base):
    __tablename__ = "platform_users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_photo_url: Mapped[str] = mapped_column(String(1024), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    country_code: Mapped[str] = mapped_column(String(10), nullable=True)
    join_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_active_time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_suspended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    entitlements: Mapped[list["UserEntitlement"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class UserEntitlement(Base):
    __tablename__ = "user_entitlements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("platform_users.telegram_id"), nullable=False, index=True)
    active_plan: Mapped[PlanType] = mapped_column(Enum(PlanType), default=PlanType.FREE, nullable=False)
    unlocked_features: Mapped[list] = mapped_column(JSON, default=lambda: [], nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["PlatformUser"] = relationship(back_populates="entitlements")

class GlobalFeatureToggle(Base):
    __tablename__ = "global_feature_toggles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    feature_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
