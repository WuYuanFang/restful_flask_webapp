from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from App.Model.model import User


# 定义检测是否需要登录验证的装饰器
def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return check_login


# 定义检测token是否过期的装饰器
def check_token(func):
    @wraps(func)
    def token_check(*args, **kwargs):
        if request.method == 'POST':
            token = request.form.get('token')
        else:
            token = request.args.get('token')
        user = User.verify_token(token)
        if user is None:
            return jsonify(data='', msg='token过期', success=False)
        else:
            return func(*args, **kwargs)
    return token_check


# 检测参数是否为空
def all_not_null(*args):
    for tmp in args:
        if not tmp:
            return False
    return True

