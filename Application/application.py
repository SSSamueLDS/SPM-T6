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

class Application(db.Model):
    __tablename__ = 'Application'

    application_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_ID = db.Column(db.Integer, nullable=False)
    role_ID = db.Column(db.Integer, nullable=False)
    date_applied = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Rejected', 'Under Review', 'Withdrawn'), nullable=False)

    def json(self):
        dto = {
            'application_ID': self.application_ID,
            'staff_ID': self.staff_ID,
            'role_ID': self.role_ID,
            'date_applied': self.date_applied.strftime('%Y-%m-%d'),  # Format date as string
            'status': self.status,
        }
        return dto


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)