from flask_restful import Resource
from flask import jsonify


# 用户
class UserRes(Resource):
    def post(self):
        pass

    def get(self):
        return jsonify(data='test', msg='测试', success=True)
