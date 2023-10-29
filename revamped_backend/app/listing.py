import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Skill, Listing, ListingSkill

from datetime import datetime
import json
from os import environ
import argparse
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

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
        listing = Listing.query.filter_by(listing_id=listing_id).first()
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
        listing = Listing.query.filter_by(listing_id=listing_id).first()
        if not listing:
            return jsonify(
                {
                    "code": 404,
                    "data": {"listing_id": listing_id},
                    "message": "listing not found."
                }
            ), 404

        data = request.get_json()
        listing.listing_name = data.get('listing_name')
        listing.listing_description = data.get('listing_description')
        listing.dept = data.get('dept')
        listing.deadline = data.get('deadline')

        try:
            ListingSkill.query.filter_by(listing_id=listing_id).delete()

            new_listing_skills = [ListingSkill(listing_id=listing_id, skill_id=skill_id) for skill_id in data.get('listing_skill')]
            db.session.bulk_save_objects(new_listing_skills)
            
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating the listing and its skills: " + str(e)
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": listing.json()
            }
        )

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
        listing_skills = []
        for skill_id in skill_ids:
            new_listing_skill = ListingSkill(listing_id=listing_id, skill_id=skill_id)
            listing_skills.append(new_listing_skill)

        try:
            db.session.bulk_save_objects(listing_skills)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new listing skills: " + str(e)
                }
            ), 500

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
    main()
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)
