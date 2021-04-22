from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:zaq11403@localhost:3306/taipeiprojectdb'
db = SQLAlchemy(app)

class attraction_tb(db.Model):
    __table_args__ = {
        'comment': 'Notice table',
        'extend_existing': True
    }
    id = db.Column(db.Integer, primary_key = True, comment='編號')
    name = db.Column(db.String(50), nullable = False, comment = '景點名稱') 
    category = db.Column(db.String(50), nullable = False, comment = '景點分類') 
    description = db.Column(db.Text, nullable = False, comment = '景點介紹') 
    address = db.Column(db.String(255), nullable = False, comment = '地址') 
    transport = db.Column(db.Text, comment = '交通資訊') 
    mrt = db.Column(db.String(50), comment = '捷運') 
    latitude = db.Column(db.Numeric(9,6), nullable = False, comment = '經度') 
    longitude = db.Column(db.Numeric(9,6), nullable = False, comment = '緯度') 
    images = db.Column(db.Text, nullable=False , comment = '景點照片')
    
    def __init__ (self,id,name,category,description,address,transport,mrt,latitude,longitude,images):
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.latitude = latitude
        self.longitude = longitude
        self.images = images