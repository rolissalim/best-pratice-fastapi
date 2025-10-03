
from fastapi import HTTPException
from app.base import *
from app.models.user_model import User, UserToken
from app.config.security import verify_password, create_access_token, str_encode,get_token_payload
from app.schemas.auth_shema import TokenSchema
from app.utils.util import unique_string
from app.config.setting import get_settings
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta

settings = get_settings()

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
class AuthService(BaseService):

    async def login(self, user_login, db):
        user = User.check_user_login(user_login.username, db)
        if not user:
            raise HTTPException(status_code=400, detail="Username or password is wrong.")
        
        if not verify_password(user_login.password, user.password):
            raise HTTPException(status_code=400, detail="Username or password is wrong")

        return AuthService._generate_tokens(user, db)

    def _generate_tokens(user, db) -> TokenSchema:
        # generate keys
        refresh_key = unique_string(100)
        access_key = unique_string(50)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES, hours=-7)

        expires_at = datetime.now() + refresh_token_expires

        # simpan refresh token ke DB
        user_token = UserToken(
            user_id=str(user.id),   # ✅ pastikan string, bukan UUID
            refresh_key=refresh_key,
            access_key=access_key,
            expires_at=expires_at
        )
        db.add(user_token)
        db.commit()
        db.refresh(user_token)

        # access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES, hours=-7)
        access_token = create_access_token(
            {
                "user_id": str(user.id),       # ✅ convert UUID ke string
                "a": access_key,
                "r": str_encode(str(user_token.id)),
                "n": str_encode(user.name),
            },
            expiry=access_token_expires,
        )

        # refresh token
        refresh_token = create_access_token(
            {
                "user_id": str(user.id),   # ✅ convert UUID ke string
                "t": refresh_key,
                "a": access_key,
            },
            expiry=refresh_token_expires,
        )

        return TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"   # ✅ tambahkan biar sesuai OAuth2
    ) 
    
    def refresh_access_token(refresh_token: str, db) -> TokenSchema:
        payload = get_token_payload(refresh_token)

        user_id = payload.get("user_id")
        t = payload.get("t")
        a = payload.get("a")

        if not user_id or not t:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Cek di DB kalau kamu simpan refresh key
        user_token = db.query(UserToken).filter_by(user_id=user_id, refresh_key=t, access_key=a).first()
        if not user_token or user_token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

        # Generate token baru
        return AuthService._generate_tokens(user_id, a, t)

        
