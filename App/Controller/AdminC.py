from flask_restful import reqparse, marshal, fields
from utils.tools import result, all_not_null
from .BaseResource import Resource
from ..Model.model import User
from App import db

parse = reqparse.RequestParser()
parse.add_argument('page', type=int, default=1)
parse.add_argument('size', type=int, default=20)
parse.add_argument('name', type=str)
parse.add_argument('old_name', type=str)


user_field = {
    'u_id': fields.Integer,
    'username': fields.String,
    'u_create_time': fields.DateTime
}


# 用户
class Admin(Resource):

    def get(self):
        # res = db.session.execute('select * from user').fetchall()
        # for r in res:
        #     print(r.u_id, r.username)
        args = parse.parse_args()
        name = args.get('name')
        page = args.get('page')
        size = args.get('size')
        if all_not_null(name):
            user = User.query.filter_by(username=name).first()
            if user:
                return result('请求成功', True, marshal(user, user_field))
        else:
            users = User.query.paginate(page, per_page=size)
            return result('请求成功', True, marshal(users.items, user_field), page=page, total=users.total)

    def delete(self):
        args = parse.parse_args()
        name = args.get('name')
        if not all_not_null(name):
            return result('参数不能为空')
        user = User.query.filter_by(username=name).first()
        if user is None:
            return result('用户不存在')
        else:
            try:
                db.session.delete(user)
                db.session.commit()
                return result('删除成功', True)
            except Exception as e:
                db.session.rollback()
                return result(e.message)

    def put(self):
        args = parse.parse_args()
        name = args.get('name')
        old_name = args.get('old_name')
        if not all_not_null(name, old_name):
            return result('参数不能为空')
        user = User.query.filter_by(username=old_name).first()
        if user is None:
            return result('用户不存在')
        else:
            user.username = name
            user.save()
            return result('修改成功', True)




