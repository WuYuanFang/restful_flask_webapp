from App import api
from .LoginC import LoginRes

api.add_resource(LoginRes, '/phone/login')

