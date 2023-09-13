import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class SystemRole(db.Model):
    __tablename__ = 'System_Role'

    systemrole_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    systemrole_name = db.Column(db.String(50), nullable=False, unique=True)

    def json(self):
        dto = {
            'systemrole_ID': self.systemrole_ID,
            'systemrole_Name': self.systemrole_name,
        }
        return dto


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)