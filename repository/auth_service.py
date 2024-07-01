from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import requests

class AoutService(ABC):
    @abstractmethod
    def get_uri(self,  query_parameter: str):
        """
            Generate a URI for OAuth2 token request.
            This function uses the provided parameters to construct a URI for making an OAuth2 token request.
        Args:
            query_parameter (str): The authorization state.
            base_url (str): The base URL to which the token request should be sent.

        Returns:
            str: The generated URI for making the token request.
        """
    @abstractmethod    
    def get_access_token(self, code: str, redirect_url: str, url: str) -> str:
        """
        Obtain an access token using the provided credentials.
        Args:
            code (str): This parameter appears to be the authorization code that was obtained as a result of the user granting access to your application during the OAuth2 flow. .
            redirect_url(str) : This is typically the URL where the user should be redirected after the OAuth2 flow is completed. 
        Returns:
            str: The access token.
        """
    
   
        