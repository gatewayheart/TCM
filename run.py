from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

POSTGRES={}
POSTGRES = {
    'user': 'postgres',
    'pw': 'Cotec*123',
    'db': 'postgres',
    'host': '192.168.1.2',
    'port': '5432'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'


db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return models.RevokedTokenModel.is_jti_blacklisted(jti)

import views, resources
# api.add_resource(resources.PhanVungDichTe, '/PhanVungDichTe')
api.add_resource(resources.EpidemiologicalZoning, '/EpidemiologicalZoning')
api.add_resource(resources.layNguonNuoc, '/layNguonNuoc')
# api.add_resource(resources.getPerTopDisease,'/disease_model/top_10_diseases')


