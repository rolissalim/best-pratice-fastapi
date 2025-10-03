from fastapi import APIRouter
from typing import Optional
from app.config.setting import get_settings
import logging
settings = get_settings()

class BaseRouter:
    
    def __init__(self, module:Optional[str] = None, dependencies:Optional[list] = None):
        self.module = module
        self.dependencies = dependencies


    def get_router(self):
        return APIRouter(
            prefix=f"/{self.format_module(self.module)}",
            tags=[f"{self.module}"],
            responses={404: {"description": "Not found"}},
            dependencies=self.dependencies if self.dependencies is not None else None
        )
    
    
    def format_module(self, str) -> str:
        if str is None:
            return f"{self.version()}"
        return f"{self.version()}/{str.lower().replace(' ','-')}"



    def version(self) -> str:
        return settings.VERSION