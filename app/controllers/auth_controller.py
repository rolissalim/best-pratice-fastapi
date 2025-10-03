from fastapi import HTTPException, status
from app.base import *
from app.schemas.auth_shema import UserRegisterSchema
from app.schemas.auth_shema import TokenSchema,RefreshToken
from app.schemas.user_schema import UserReadSchema
from app.dependency.deps import (
    db_dependency, 
    user_service_dependency, 
    oauth2_request_form_dependency, 
    auth_service_dependency,
    current_user_dependency
)
import urllib.parse

class AuthController(BaseRouter):
    base_router = BaseRouter(module="Auth")
    router = base_router.get_router()

    @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[UserReadSchema])
    async def register_user(
        create_schema: UserRegisterSchema,
        db: db_dependency, 
        service: user_service_dependency,
    ):
        try:
            create_schema.role_id=3
            data = await service.create_user(create_schema, db)
            return response_json(
                message=f"Successfully register new user",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e, create_schema)
        
    
    @router.post("/login", response_model=TokenSchema)
    async def login(
        user_login: oauth2_request_form_dependency, 
        db: db_dependency, 
        service: auth_service_dependency
    ):
        try:
            return await service.login(user_login, db)
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e)

    
    # @router.get("/google/login")
    # def google_login():
    #     base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    #     params = {
    #         "client_id": settings.GOOGLE_CLIENT_ID,
    #         "response_type": "code",
    #         "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    #         "scope": "openid email profile",
    #         "access_type": "offline",
    #         "prompt": "consent"
    #     }
    #     url = f"{base_url}?{urllib.parse.urlencode(params)}"
    #     return {"auth_url": url}
    
    # @router.get("/google/callback")
    # def google_callback(code: str, db: db_dependency,service: auth_service_dependency):
    #     # Tukar code dengan access_token
    #     token_url = "https://oauth2.googleapis.com/token"
    #     data = {
    #         "code": code,
    #         "client_id": settings.GOOGLE_CLIENT_ID,
    #         "client_secret": settings.GOOGLE_CLIENT_SECRET,
    #         "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    #         "grant_type": "authorization_code",
    #     }
    #     r = requests.post(token_url, data=data)
    #     token_data = r.json()

    #     if "access_token" not in token_data:
    #         raise HTTPException(status_code=400, detail="Google login failed")

    #     # Ambil data user
    #     user_info = requests.get(
    #         "https://www.googleapis.com/oauth2/v2/userinfo",
    #         headers={"Authorization": f"Bearer {token_data['access_token']}"}
    #     ).json()

    #     email = user_info["email"]
    #     name = user_info.get("name")

    #     # Cek di DB, kalau belum ada → register
    #     user = db.query(User).filter(User.email == email).first()
    #     if not user:
    #         user = User(
    #             email=email,
    #             name=name,
    #             password=None,  # karena login via Google
    #             role_id=None
    #         )
    #         db.add(user)
    #         db.commit()
    #         db.refresh(user)

    #     # Generate access & refresh token lokal (punya kita)
    #     return service._generate_tokens(user, db)
         
    @router.post("/refresh", response_model=TokenSchema)
    async def refresh_token(
        request: RefreshToken,
        db: db_dependency,
        service: auth_service_dependency
    ):
        return service.refresh_access_token(request.refresh_token, db)
    
    @router.get("/me")
    async def read_me(current_user=current_user_dependency):
        return current_user
    # def read_me(current_user: User = Depends(get_current_user)):
    #     return {
    #         "id": str(current_user.id),
    #         "username": current_user.username,
    #         "name": current_user.name,
    #         "email": current_user.email,
    #     }