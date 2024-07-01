from typing import Dict, Type
from services.user_services.google_aout import GoogleOauth2Service
from repository.auth_service import AoutService

service_dict: Dict[str, Type[AoutService]] = {
    "google_auth": GoogleOauth2Service
}