import time
import jwt
from config.settings import settings
from typing import Optional, Dict, Any

def token_response(token: str) -> Dict[str, str]:
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    """Create a JWT token for the user"""
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600,  # 1 hour expiration
        "iat": time.time()  # issued at
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token_response(token)

def decodeJWT(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate JWT token"""
    try:
        if not token:
            return None
            
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Check if token is expired
        if decoded_token["expires"] < time.time():
            return None
            
        return decoded_token
        
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None

def is_token_expired(token: str) -> bool:
    """Check if token is expired without raising exceptions"""
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
        return decoded["expires"] < time.time()
    except:
        return True