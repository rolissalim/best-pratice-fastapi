from typing import Annotated, Union, Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from app.config.database import get_session
from app.config.security import get_current_user,oauth2_scheme

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

class CommonQueryParams:
    def __init__(
        self, 
        keywords: Union[str, None] = None, 
        page: int = 1, 
        limit: int = 10,
    ):
        self.keywords = keywords
        self.page = page
        self.limit = limit

class DashboardParams:
     def __init__(
        self, 
        partai_id: Optional[int] = None,
        status_ids: Optional[str] = None,
        anggota_id: Optional[int] = None,
        workspace_id: Optional[str] = None,
        user_id: Optional[str] = None,
        city_id: Optional[str] = None,
        district_id: Optional[str] = None,
        start_date: Union[datetime, None] = None, 
        end_date: Union[datetime, None] = None, 
        year:Optional[str]=None
    ):
        self.partai_id = partai_id
        self.status_ids = status_ids
        self.anggota_id = anggota_id
        self.city_id = city_id
        self.district_id = district_id
        self.workspace_id=workspace_id
        self.user_id=user_id
        self.start_date = start_date
        self.end_date = end_date
        self.year = year


class DashboardCityParams:
     def __init__(
        self, 
        kabupaten_id: Optional[str] = None,
        year: Optional[str] = None,
    ):
        self.kabupaten_id = kabupaten_id
        self.year = year



class DashboardSubdistrictParams:
     def __init__(
        self, 
        subdistrict_id: Optional[str] = None,
        year: Optional[str] = None,
    ):
        self.subdistrict_id = subdistrict_id
        self.year = year

class DashboardVillageParams:
     def __init__(
        self, 
        village_id: Optional[str] = None,
        year: Optional[str] = None,
    ):
        self.village_id = village_id
        self.year = year

# dependencies common param
common_params_dependency = Annotated[CommonQueryParams, Depends(CommonQueryParams)]
dashboard_params_dependency = Annotated[DashboardParams, Depends(DashboardParams)]
dashboard_params_city_dependency = Annotated[DashboardCityParams, Depends(DashboardCityParams)]
dashboard_params_subdistrict_dependency = Annotated[DashboardSubdistrictParams, Depends(DashboardSubdistrictParams)]
dashboard_params_village_dependency = Annotated[DashboardVillageParams, Depends(DashboardVillageParams)]

# dependencies database
db_dependency = Annotated[Session, Depends(get_session)]
# db_dependency_p2024 = Annotated[Session, Depends(get_session_p2024)]

# dependencies service
auth_service_dependency = Annotated[Session, Depends(AuthService)]
user_service_dependency = Annotated[Session, Depends(UserService)]

# dependencies current user
oauth2_dependency = Depends(oauth2_scheme)
current_user_dependency = Depends(get_current_user)

# dependencies oauth2 request form
oauth2_request_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
