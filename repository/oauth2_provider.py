from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import requests

from repository.auth_service import AoutService

class OAuth2Provider(AoutService, ABC):
    @abstractmethod
    def get_google_provider_cfg(self):
        """
        Retrieve Google OAuth2 provider configuration.

        This function sends an HTTP GET request to the Google Discovery URL to obtain the configuration
        details required for implementing Google OAuth2 authentication.

        Returns:
            requests.Response: The HTTP response containing the Google OAuth2 provider configuration.
        """
    @abstractmethod   
    def request_uri(self, endpoint: str, parameter: Optional[str] = None, parameter_name:Optional[str] = None) -> str:
        """
        This code appears to be constructing a URL for making a request to the OAuth2 token endpoint. Here's what each parameter does:.

        Args:
            role (str, optional): The role to be included as a query parameter.

        Returns:
            str: The generated URI.
        """
        
    @abstractmethod
    def request_uri(self, code:str, redirect_url:str = None) -> str:
        """
        This code appears to be constructing a URL for making a request to the OAuth2 token endpoint. Here's what each parameter does:.

        Args:
            code (str): This parameter appears to be the authorization code that was obtained as a result of the user granting access to your application during the OAuth2 flow. .
            redirect_url(str) : This is typically the URL where the user should be redirected after the OAuth2 flow is completed. 
        Returns:
            str: The generated URI.
        """
    @abstractmethod
    def get_user_info(self, code: str)-> Dict[str, Any]:
         """
        Perform a POST request to obtain a Google OAuth2 token.
        This function sends a POST request to the specified token endpoint to exchange the
        authorization code for an OAuth2 token.

        Args:
            token_endpoint (str): The OAuth2 token endpoint URL.
            code (str): The authorization code received during the OAuth2 flow.

        Returns:
            requests.Response: The HTTP response containing the OAuth2 token.
        """

    
   
        