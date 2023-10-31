import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Application, Staff, Skill, Role, RoleSkill, StaffSkill, AccessControl

from datetime import date, datetime
import json
from os import environ
import argparse
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="select env")
    parser.add_argument("-test", action="store_true", help="Enable the test env")
    parser.add_argument("-prod", action="store_true", help="Enable the prod env")
    args = parser.parse_args()

    
    if args.test:
        print("test env")
        dbURL = os.getenv("testdbURL")
        
        
    elif args.prod:
        
        print("prod env")
        dbURL = os.getenv("proddbURL")
        
    else:
        print("Please Specify the environment.")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = dbURL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    CORS(app)

    @app.route('/apply', methods=['POST'])
    def apply_for_listing():
        data = request.json
        staff_id = data.get('staff_id')
        listing_id = data.get('listing_id')
        staff_name = data.get('staff_name')

        # Check if an application with the same staff_id and listing_id already exist
        existing_application = Application.query.filter_by(staff_id=staff_id, listing_id=listing_id, staff_name=staff_name).first()
        if existing_application:
            return jsonify({"message": "You've already applied for this listing.", "error": True}), 400  # Directly return the error message

        # If not, proceed to add the application
        application = Application(staff_id=staff_id, listing_id=listing_id,staff_name=staff_name,date_applied=date.today())
        db.session.add(application)
        db.session.commit()

        return jsonify(application.json()), 201

    @app.route("/applications", methods=['GET'])
    def get_all_applications():
        # fetch all roles from the database
        applications = Application.query.all()
        if applications:
            return jsonify({
                "code": 200,
                "data": [application.json() for application in applications]
            })
        return jsonify({
            "code": 404,
            "message": "No applications found.",
            "data": []
        })

    @app.route("/listings/<int:listing_id>/applications", methods=['GET'])
    def get_applications_by_listing(listing_id):
        # fetch all applications for a specific listing from the database
        applications = Application.query.filter_by(listing_id=listing_id).all()
        if applications:
            return jsonify({
                "code": 200,
                "data": [application.json() for application in applications]
            })
        return jsonify({
            "code": 404,
            "message": "No applications found for this listing.",
            "data": []
        })

    @app.route("/applications/<int:application_id>", methods=['GET'])
    def get_application_by_id(application_id):
        # fetch the application with the specific application_id from the database
        application = Application.query.get(application_id)
        if application:
            return jsonify({
                "code": 200,
                "data": application.json(),
            })
        return jsonify({
            "code": 404,
            "message": "Application not found.",
            "data": []
        })


if __name__ == '__main__':
    main()
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5006, debug=True)