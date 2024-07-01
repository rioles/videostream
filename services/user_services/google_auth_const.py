class GoogleOAuthConstants:
    # Static constants
    
    __REDIRECT_URI = 'https://d9b2-156-0-214-24.ngrok-free.app/api/v1/login/callback/google'
    #__REDIRECT_URI = 'http://127.0.0.1:5000/api/v1/login/callback/google'
    __DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    # Static method to get redirect_uri
    @staticmethod
    def get_redirect_uri():
        return GoogleOAuthConstants.__REDIRECT_URI

    # Static method to get discovery_url
    @staticmethod
    def get_discovery_url():
        return GoogleOAuthConstants.__DISCOVERY_URL
        
        
#__REDIRECT_URI = 

