## What this is

A FastAPI-based backend for a content creator platform that manages user authentication via Telegram, subscription tiers, feature entitlements, and dynamic feature toggles. It handles creator monetization with progressive pricing discounts and provides Telegram-integrated authentication with JWT token validation.

### Stack

- **Language(s):** Python (95.8%) + Docker (4.2%)
- **Framework / runtime:** FastAPI + Uvicorn, PostgreSQL + async SQLAlchemy, Redis, Telegram Bot API
- **Notable libraries:** aiogram (Telegram integration), asyncpg (async PostgreSQL), pydantic (validation), PyJWT (token management), yt-dlp (video downloading)

## How it's organized

```
src/
  api/v1/
    auth_endpoints.py        Telegram login endpoint, user registration
    subscription_endpoints.py Subscription & feature access control routes
  auth/
    telegram_auth.py         Telegram WebApp data validation (HMAC-SHA256)
    jwt_handler.py           JWT token creation & verification (7-day expiry)
  services/
    pricing_engine.py        Progressive bulk-bundle discount calculator
    toggle_registry.py       Feature flag registry with Redis caching (5min TTL)
  models/
    subscription_models.py   SQLAlchemy ORM: PlatformUser, UserEntitlement, GlobalFeatureToggle
  config.py                  Environment configuration via pydantic-settings
  database.py                Async PostgreSQL setup with SQLAlchemy
  main.py                    FastAPI app initialization, lifespan, middleware

docker/
  app.Dockerfile             Python 3.11+ slim image, uvicorn runner
  nginx.conf                 Reverse proxy configuration

docker-compose.yml           PostgreSQL 16, Redis 7, FastAPI service orchestration
requirements.txt             Dependencies (fastapi, sqlalchemy, asyncpg, redis, jwt, etc.)
```

**How it fits together:** When a user hits `/api/v1/auth/telegram-login`, the TelegramAuthValidator cryptographically verifies the Telegram WebApp init data using HMAC-SHA256. On first login, a new PlatformUser and FREE-tier UserEntitlement are created in PostgreSQL. The JWTManager then issues a 7-day JWT token. Protected routes like `/api/v1/subscription/creator-dashboard` verify the JWT and check feature toggles via ToggleRegistryService, which caches toggle state in Redis for 5 minutes before falling back to the database. The PricingEngine computes sliding discounts (up to 40%) for bulk subscription purchases.

## How to run it

```bash
# Using Docker Compose (recommended)
docker-compose up --build

# The API will be available at http://localhost:8000
# Postgres at localhost:5432, Redis at localhost:6379
```

For development without Docker:
```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/aicreatorhub"
export REDIS_URL="redis://localhost:6379/0"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export JWT_SECRET_KEY="your_secret_key"
uvicorn src.main:app --reload
```
