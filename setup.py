from setuptools import setup, find_packages

setup(name="vid_stream",
      version='0.0.1',
      packages=['api/v1/endpoints','services','api','domain','infrastructure', 'models', 'models/engine', 'repository',
                'domain/user', 'tests', 'tests/models', 'tests/services', 'tests/api',
                'services/user_services','api/v1/endpoints/user', 'api.v1','dto'])