import flask_restful
from functools import wraps
from flask import request, jsonify
from App.Model.model import User


# 请求的auth验证
def authenticate(func):
    @wraps(func)
    def token_check(*args, **kwargs):
        print('method : %s' % func.__name__)
        # 在这里获取请求相关的数据,如果参数中，包含token并且有效，才允许网下执行，但是登录跟注册接口例外,把例外的接口单独抽出 来，
        except_resource = ['login', 'register']
        request_url = request.url
        request_url_arr = request_url.split('/')
        last_index = len(request_url_arr)
        if request_url_arr[last_index - 1] in except_resource:
            return func(*args, **kwargs)
        else:
            # 不再列表中，需要验证
            token = str(request.headers.get('token'))
            user = User.verify_token(token)
            if user is None:
                return jsonify(data='', msg='token过期', success=False)
            else:
                return func(*args, **kwargs)
    return token_check


class Resource(flask_restful.Resource):
    method_decorators = [authenticate]
