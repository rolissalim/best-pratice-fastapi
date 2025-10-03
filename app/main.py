from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.base.base_error import custom_validation
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


def create_application():
    application = FastAPI(
        title="Recruitment Employee API",
        description="Documentation Recruitment Employee API v0.1",
        version="0.1",
        swagger_ui_parameters={"operationsSorter": "method"},
    )

    # Mount the directory containing static files
    application.mount("/public", StaticFiles(directory="public"), name="public")

    application.include_router(AuthController.router)
    application.include_router(UserController.router)
    
    
    return application

app = create_application()

# Menambahkan middleware CORSdoc
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin (tidak disarankan untuk produksi)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_response = await custom_validation(exc)
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    # logging.error(msg="value error", extra={"data":str(exc)})
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
    