class GoogleOAuthConfig:
    def __init__(self, builder):
        self.__client_id = builder._Builder__client_id
        self.__client_secret = builder._Builder__client_secret
        self.__discovery_url = builder._Builder__discovery_url
        self.__redirect_url = builder._Builder__redirect_url
        self.__password = builder._Builder__password

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def discovery_url(self):
        return self.__discovery_url

    @property
    def redirect_url(self):
        return self.__redirect_url
    
    @property
    def password(self):
        return self.__password

    class Builder:
        def __init__(self):
            self.__client_id = None
            self.__client_secret = None
            self.__discovery_url = None
            self.__redirect_url = None
            self.__password = None

        def client_id(self, client_id):
            self.__client_id = client_id
            return self

        def client_secret(self, client_secret):
            self.__client_secret = client_secret
            return self

        def discovery_url(self, discovery_url):
            self.__discovery_url = discovery_url
            return self

        def redirect_url(self, redirect_url):
            self.__redirect_url = redirect_url
            return self
            
        def password(self, password):
            self.__password = password
            return self

        def build(self):
            return GoogleOAuthConfig(self)


