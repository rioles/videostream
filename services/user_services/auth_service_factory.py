from typing import Any, Type, Dict
from dto.auth_config_dto import GoogleOAuthConfig
from repository.auth_service import AoutService


class AuthServiceFactory:
    
    @staticmethod
    def create_service(service_type: str, config:GoogleOAuthConfig, service: Dict[str, Type[AoutService]]) -> AoutService:
        service_class = service.get(service_type)
        if not service_class:
            raise ValueError(f"Unknown service type: {service_type}")
        return service_class(config)
    
