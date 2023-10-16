import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Skill, Listing, ListingSkill

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.route("/create_listing", methods=['POST'])
def create_listing():
        
        data = request.get_json()
        print(data)

        listing_name = data.get('listing_name')
        listing_description = data.get('listing_description')
        deadline = data.get('deadline')
        dept = data.get('dept')
        hr_id = data.get('hr_id')

        new_listing = Listing(listing_name=listing_name, listing_description=listing_description, dept=dept, deadline=deadline, hr_id=hr_id)

        try:
            db.session.add(new_listing)
            db.session.commit()
            create_listing_skill(data.get('listing_skill'), new_listing.listing_id)
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new listing : " + str(e)
                }
            ), 500

        return jsonify(
            {
                "code": 201,
                "data": new_listing.json()
            }
        ), 201

@app.route("/listings", methods=['GET'])
def get_all_listings():
    # fetch all listings from the database
    listings = Listing.query.all()
    if listings:
        return jsonify({
            "code": 200,
            "data": [listing.json() for listing in listings]
        })
    return jsonify({
        "code": 404,
        "message": "No listings found."
    })

@app.route("/listings/<int:listing_id>", methods=['GET'])
def get_listing(listing_id):
    # fetch listing by id
    listing = listing.query.filter_by(listing_id=listing_id).first()
    print(listing)
    skill_ids = get_skill_ids_by_listing(listing_id)
    print(skill_ids)
    if listing:
        return jsonify({
            "code": 200,
            "data": {
                **listing.json(),
                "skill_ids": skill_ids
            }
        })
    return jsonify({
        "code": 404,
        "message": "No listing with id " + listing_id +  "found."
    })

@app.route("/update_listing/<int:listing_id>", methods=['PUT'])
def update_listing(listing_id):
    listing = listing.query.filter_by(listing_id=listing_id).first()
    if listing:
        data = request.get_json()
        listing.listing_name = data.get('listing_name')
        listing.listing_description = data.get('listing_description')
        listing.deadline = data.get('deadline')
        db.session.commit()
        update_listing_skill(skill_ids=data.get('listing_skill'), listing_id=listing_id)

        return jsonify(
            {
                "code": 200,
                "data": listing.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "listing_id": listing_id
            },
            "message": "listing not found."
        }
    ), 404

# This is to create a new skill
@app.route('/skill', methods=['POST'])
def create_skill():
    data = request.get_json()
    skill_name = data.get('skill_name')

    new_skill = Skill(skill_name = skill_name)

    try:
        db.session.add(new_skill)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding new skill : " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_skill.json()
        }
    ), 201

# This is to find all the skills given specific listing id
@app.route("/listing_skill/<int:listing_id>", methods=['GET'])
def get_skills_by_listing(listing_id):
    try:
        listing_skills = ListingSkill.query.filter_by(listing_id=listing_id).all()
        skills = [listing_skill.skill_id for listing_skill in listing_skills]
        if listing_skills:
            return jsonify({
                "code": 200,
                "data": {
                    "listing_id": listing_id,
                    "skill_ids": skills
                }
            })
        return jsonify({
            "code": 404,
            "message": "No skills found for the given listing id."
        }), 404

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({
            "code": 500,
            "message": "Internal Server Error"
        }), 500

@app.route('/listing_skill', methods =['GET'])
def get_all_listing_skill():
    listing_skills = ListingSkill.query.all()
    listing_skill_map = {}
    
    for ls in listing_skills:
        if ls.listing_id not in listing_skill_map:
            listing_skill_map[ls.listing_id] = []
        listing_skill_map[ls.listing_id].append(ls.skill_id)

    return jsonify(
        {
            "code": 201,
            "data": listing_skill_map
        }
    ), 201

def get_skill_ids_by_listing(listing_id):
    try:
        listing_skills = ListingSkill.query.filter_by(listing_id=listing_id).all()
        skills = [listing_skill.skill_id for listing_skill in listing_skills]
        if listing_skills:
            return skills
        return []

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({
            "code": 500,
            "message": "Internal Server Error"
        }), 500

def create_listing_skill(skill_ids, listing_id):
    for skill_id in skill_ids:
        new_listing_skill = ListingSkill(listing_id = listing_id, skill_id = skill_id)
        try:
            db.session.add(new_listing_skill)
            db.session.commit()
            print('new entry commited')
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new listing skill" + str(e)
                }
            ), 500
        
        print(json.dumps(new_listing_skill.json(), default=str)) # convert a JSON object to a string and print
        print()

    return jsonify(
        {
            "code": 201,
            "data": {
                "listing_id": listing_id,
                "skill_ids": skill_ids 
            }
        }
    ), 201

def update_listing_skill(skill_ids, listing_id):
    # Delete all existing listing-skill mappings for the given listing
    try:
        ListingSkill.query.filter_by(listing_id=listing_id).delete()
        db.session.commit()
    except Exception as e:
        return jsonify({"code": 500, "message": f"An error occurred while deleting old listing skills: {str(e)}"}), 500

    # Add new listing-skill mappings
    for skill_id in skill_ids:
        new_listing_skill = ListingSkill(listing_id = listing_id, skill_id = skill_id)
        try:
            db.session.add(new_listing_skill)
            db.session.commit()
            print('new entry commited')
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new listing skill" + str(e)
                }
            ), 500
        
        print(json.dumps(new_listing_skill.json(), default=str)) # convert a JSON object to a string and print
        print()

    return jsonify(
        {
            "code": 201,
            "data": {
                "listing_id": listing_id,
                "skill_ids": skill_ids 
            }
        }
    ), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)
