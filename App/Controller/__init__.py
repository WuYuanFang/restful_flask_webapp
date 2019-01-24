from App import api
from .LoginC import LoginRes
from .RegiterC import Register
from .AdminC import Admin

api.add_resource(LoginRes, '/phone/login')
api.add_resource(Register, '/phone/register')
api.add_resource(Admin, '/phone/user')
