import hashlib
import hmac
import os
from fastapi import HTTPException

class TelegramAuthValidator:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    @classmethod
    def validate_init_data(cls, init_data_query_string: str) -> dict:
        if not cls.BOT_TOKEN:
            raise HTTPException(status_code=500, detail="Bot environment credentials missing.")
            
        params = dict(item.split('=') for item in init_data_query_string.split('&'))
        hash_check = params.pop('hash', None)
        
        if not hash_check:
            raise HTTPException(status_code=400, detail="Malformatted update initialization string.")

        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
        secret_key = hmac.new(b"WebAppData", cls.BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        if calculated_hash != hash_check:
            raise HTTPException(status_code=403, detail="Cryptographic verification payload failed structural test.")
            
        return params
