import json
import os
from typing import Any, Dict, Optional, Union
import uuid
import requests
from dto.auth_config_dto import GoogleOAuthConfig
from dotenv import load_dotenv
import os 
from flask import request
from repository.oauth2_provider import OAuth2Provider
from services.user_services.google_auth_const import GoogleOAuthConstants
import threading
import requests
from oauthlib.oauth2 import WebApplicationClient
load_dotenv()
client = WebApplicationClient(f"{os.environ.get('GOOGLE_CLIENT_ID')}")
class GoogleOauth2Service(OAuth2Provider):
    __instance = None
    __lock = threading.Lock()

    def __new__(cls,*args, **kwargs):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(GoogleOauth2Service, cls).__new__(cls)
                cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, config:GoogleOAuthConfig):
        if self.__initialized:
            return
        self.config = config
        self.__initialized = True
        
    def get_google_provider_cfg(self)-> requests.Response:
        """
        Retrieve Google OAuth2 provider configuration.

        This function sends an HTTP GET request to the Google Discovery URL to obtain the configuration
        details required for implementing Google OAuth2 authentication.

        Returns:
            requests.Response: The HTTP response containing the Google OAuth2 provider configuration.
        """
        return requests.get(self.config.discovery_url)
    
    def get_uri(self, query_parameter: str):
        """
            Generate a URI for OAuth2 token request.
            This function uses the provided parameters to construct a URI for making an OAuth2 token request.
        Args:
            query_parameter (str): The authorization state received during the OAuth2 flow.
            base_url (str): The base URL to which the token request should be sent.

        Returns:
            str: The generated URI for making the token request.
        """
        
        google_provider_cfg = self.get_google_provider_cfg().json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri= self.config.redirect_url,
        scope = ['openid', 'profile', 'email'],
        state = generatestte(query_parameter)
        )
        
        return request_uri
    
    def request_uri(self, code:str) -> str:
        """
        This code appears to be constructing a URL for making a request to the OAuth2 token endpoint. Here's what each parameter does:.

        Args:
            code (str): This parameter appears to be the authorization code that was obtained as a result of the user granting access to your application during the OAuth2 flow. .
            redirect_url(str) : This is typically the URL where the user should be redirected after the OAuth2 flow is completed. 
        Returns:
            str: The generated URI.
        """
        google_provider_cfg = self.get_google_provider_cfg().json()
        token_endpoint = google_provider_cfg["token_endpoint"]
        url = client.prepare_request_uri(
            token_endpoint,
            authorization_response = request.url,
            code = code,
            redirect_url= self.config.redirect_url
        )
        
        return url
    
    def get_access_token(self, code: str) -> Optional[str]:
        """
        Obtain an access token using the provided credentials.
        Args:
            code (str): This parameter appears to be the authorization code that was obtained as a result of the user granting access to your application during the OAuth2 flow. .
            redirect_url(str) : This is typically the URL where the user should be redirected after the OAuth2 flow is completed. 
        Returns:
            str: The access token.
        """
        try:
            response = requests.post(self.request_uri(code), data={
                'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
                'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.config.redirect_url  # Use the provided redirect URL
            }, headers={'Accept': 'application/json'})

            if response.status_code == 200:
                oauth2_token = response.json().get('access_token')
                print("authe",oauth2_token)
                return oauth2_token
            else:
                print("authe",oauth2_token)
                print("Error response status code:", response.status_code)
                print("Error response content:", response.text)
                return None
        except Exception as e:
            print("Error:", e)
            return None
        
    def get_user_info(self, token: str)-> Dict[str, Any]:
        """
        Perform a POST request to obtain uder data.
        
        Args:
            oauth2_token (str): The OAuth2 token endpoint.

        Returns:
            user_dat (Dict[str, Any]): 
        """
        
        #print("my_token11", aouthoken)
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
        })
        
        return response.json()
           

    

def generatestte(parameter:str):
    uuid_str = str(uuid.uuid4())
    parameter_with_uuid = f"{uuid_str}.{parameter}"
    data = {
            "role": parameter_with_uuid
        }
    return json.dumps(data)

