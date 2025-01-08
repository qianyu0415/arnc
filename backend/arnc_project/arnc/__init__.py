# 导入flask相关
import warnings
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# 初始化实例化
app = Flask(__name__, static_folder='static')
cors = CORS(app)
jwt = JWTManager(app)

# 自定义配置文件
# app.config['STATIC_FOLDER'] = 'static'
# app.config['STATIC_URL_PATH'] = '/static'
# app.config['STATIC_HOST'] = 'http://u349276-86a4-e5e4bb69.westb.seetacloud.com'

# 配置数据库的安全
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = '123456'

app.config['JWT_SECRET_KEY'] = '123456'

# 实例化一个数据库对象
db = SQLAlchemy(app)
jwt = JWTManager(app)

warnings.filterwarnings('ignore', message='Overwriting tiny_vit_.* in registry with segment_anything.modeling.tiny_vit_sam.tiny_vit_.*')
warnings.filterwarnings('ignore', message='Detectron v2 is not installed')

from arnc import routes