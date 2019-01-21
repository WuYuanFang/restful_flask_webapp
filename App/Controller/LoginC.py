from flask_restful import Resource, reqparse, marshal, fields
from flask import jsonify
from utils.tools import all_not_null
from App.Model.model import User

parse = reqparse.RequestParser()
parse.add_argument('name')
parse.add_argument('password')


# 用户
class LoginRes(Resource):

    def post(self):
        args = parse.parse_args()
        username = args['name']
        password = args['password']
        if not all_not_null(username, password):
            return jsonify(data='', msg="数据不能为空", success=False)
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify(data='', msg="用户不存在", success=False)
        if user.verify_password(password):
            data = {'user_id': user.u_id, 'username': user.username, 'token': user.generate_token().decode('ascii')}
            return jsonify(data=data, msg='登录成功', success=True)
        else:
            return jsonify(data='', msg='登录密码错误', success=False)



