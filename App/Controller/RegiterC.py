from flask_restful import reqparse
from .BaseResource import Resource
from utils.tools import all_not_null, result
from ..Model.model import User

parse = reqparse.RequestParser()
parse.add_argument('name', type=str)
parse.add_argument('password', type=str)


class Register(Resource):

    def post(self):
        args = parse.parse_args()
        username = args.get('name')
        password = args.get('password')
        if not all_not_null(username, password):
            return result("参数不能为空")
        user = User.query.filter_by(username=username).first()
        if user:
            return result("用户名已存在")
        new_user = User(username=username, password=password)
        if new_user.save():
            return result("注册成功", True)
        else:
            return result("注册失败")


