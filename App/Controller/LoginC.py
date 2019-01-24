from flask_restful import reqparse
from flask import jsonify
from utils.tools import all_not_null, result
from App.Model.model import User
from .BaseResource import Resource

parse = reqparse.RequestParser()
parse.add_argument('name', type=str)
parse.add_argument('password', type=str)


# 用户
class LoginRes(Resource):

    def post(self):
        args = parse.parse_args()
        username = args['name']
        password = args['password']
        if not all_not_null(username, password):
            return result("参数不能为空")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return result("用户不存在")
        if user.verify_password(password):
            data = {'user_id': user.u_id, 'username': user.username, 'token': user.generate_token().decode('ascii')}
            return result('登录成功', True, data)
        else:
            return result('登录密码错误')



