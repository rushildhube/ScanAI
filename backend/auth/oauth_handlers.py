import httpx
from authlib.integrations.starlette_client import OAuth
from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pymongo.results import InsertOneResult
from config.settings import settings
from config.database import db
from auth.jwt_handler import signJWT
import secrets

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='facebook',
    access_token_url='https://graph.facebook.com/v15.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v15.0/dialog/oauth',
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    client_kwargs={'scope': 'email public_profile'}
)

async def handle_oauth_callback(provider: str, request: Request):
    try:
        if provider == 'google':
            token = await oauth.google.authorize_access_token(request)
            nonce = request.session.get('_google_nonce_')
            user_info = await oauth.google.parse_id_token(token, nonce)
            email = user_info.get('email')
            name = user_info.get('name')
        elif provider == 'facebook':
            token = await oauth.facebook.authorize_access_token(request)
            async with httpx.AsyncClient() as client:
                response = await client.get('https://graph.facebook.com/v15.0/me',
                                            params={'fields': 'id,name,email', 'access_token': token['access_token']})
            user_info = response.json()
            email = user_info.get('email')
            name = user_info.get('name')
        else:
            raise HTTPException(status_code=400, detail="Invalid OAuth provider")

        if not email:
            raise HTTPException(status_code=400, detail="Could not retrieve email from provider")

        user_collection = db.db["users"]
        existing_user = await user_collection.find_one({"email": email})

        if not existing_user:
            user_data = {
                "email": email,
                "name": name,
                "auth_provider": provider,
                "password_hash": secrets.token_hex(16),  # Dummy password hash for OAuth users
                "is_active": True
            }
            result: InsertOneResult = await user_collection.insert_one(user_data)
            user_id = str(result.inserted_id)
        else:
            user_id = str(existing_user["_id"])

        jwt_token = signJWT(user_id)
        # In a real app, you would redirect to a frontend page with the token
        return RedirectResponse(url=f"/dashboard?token={jwt_token['access_token']}", status_code=status.HTTP_302_FOUND)

    except Exception as e:
        print(f"OAuth error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during authentication")