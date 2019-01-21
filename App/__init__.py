from flask import Flask
from utils import config
import os
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 设置跨域请求
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')
app.config.from_object(config)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db = SQLAlchemy(app)
api = Api(app)
