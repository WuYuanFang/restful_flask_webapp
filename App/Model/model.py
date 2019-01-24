from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from App import app, db
from flask import jsonify


# 用户将对象转成json格式
class BaseModel(object):
    def to_json(self):
        dic = self.__dict__
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        for d in dic:
            c = dic[d]
            if isinstance(c, db.Model):
                tmp = c.to_json()
                dic[d] = tmp
        return dic


# 学生模型
class Student(db.Model, BaseModel):
    __tablename__ = 'student'
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(20), nullable=False)
    s_sex = db.Column(db.Integer)
    # 设置年级与学生一对多的关联关系
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)

    def __init__(self, s_name, s_sex, grade_id):
        self.s_name = s_name
        self.s_sex = s_sex
        self.grade_id = grade_id

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return False
        return True


# 年级模型
class Grade(db.Model, BaseModel):
    __tablename__ = 'grade'
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(20), nullable=False, unique=True)
    # 设置年级与学生一对多的关联关系
    students = db.relationship('Student', backref='grade')

    def __init__(self, name):
        self.g_name = name

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return False
        return True

    # 用户将对象转成json格式
    # def to_json(self):
    #     dict = self.__dict__
    #     if "_sa_instance_state" in dict:
    #         del dict["_sa_instance_state"]
    #     return dict


# 用户模型（用户登录使用，及权限控制）
class User(db.Model, BaseModel):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime, default=datetime.now)
    # 用户和角色的一对多关联关系
    role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))

    def __init__(self, username, password):
        self.username = username
        # 将密码通过PassLib库对密码进行hash加密
        self.password = pwd_context.encrypt(password)

    # 判断加密密码是否一样
    def verify_password(self, password1):
        return pwd_context.verify(password1, self.password)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return False
        return True

    # 生成一个token,默认有效期为1天
    def generate_token(self, expiration=86400):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({"id": self.u_id})

    # 验证token
    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


# r_p为关联表的表名
r_p = db.Table('r_p',
               db.Column('role_id', db.Integer, db.ForeignKey('role.r_id'), primary_key=True),
               db.Column('permission_id', db.Integer, db.ForeignKey('permission.p_id'), primary_key=True))


# 角色模型
class Role(db.Model, BaseModel):
    __tablename__ = 'role'
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    r_name = db.Column(db.String(20))
    # 用户和角色的一对多的关联关系
    users = db.relationship('User', backref='role')

    def __init__(self, r_name):
        self.r_name = r_name

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return False
        return True


# 权限模型
class Permission(db.Model, BaseModel):
    __tablename__ = 'permission'
    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    p_name = db.Column(db.String(16), unique=True)
    p_er = db.Column(db.String(16), unique=True)
    # 角色和权限的多对多关系
    roles = db.relationship('Role', secondary=r_p, backref=db.backref('permission', lazy=True))
