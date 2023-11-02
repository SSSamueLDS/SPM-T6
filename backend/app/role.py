from flask import jsonify, Blueprint
from .models import Role, RoleSkill

# Create a blueprint for role-related routes
role = Blueprint('role', __name__)

@role.route("/roles", methods=['GET'])
def get_all_roles():
    # Fetch all roles from the database
    roles = Role.query.all()
    if roles:
        return jsonify({
            "code": 200,
            "data": [role.json() for role in roles]
        })
    return jsonify({
        "code": 404,
        "message": "No roles found.",
        "data": []
    })

@role.route("/role_skill/<int:role_id>", methods=['GET'])
def get_skills_by_role(role_id):
    try:
        role_skills = RoleSkill.query.filter_by(role_id=role_id).all()
        print(f"Queried role_skills: {role_skills}")  # Debug print

        skills = [role_skill.skill_id for role_skill in role_skills]
        if role_skills:
            return jsonify({
                "code": 200,
                "data": {
                    "role_id": role_id,
                    "skill_ids": skills
                }
            })
        return jsonify({
            "code": 404,
            "message": "No skills found for the given role id."
        }), 404

    except Exception as e:
        print(f"Error occurred: {e}")  # Logger isn't available here, using print instead
        return jsonify({
            "code": 500,
            "message": "Internal Server Error"
        }), 500

@role.route('/role_skill', methods=['GET'])
def get_all_role_skill():
    role_skills = RoleSkill.query.all()
    role_skill_map = {}

    for rs in role_skills:
        if rs.role_id not in role_skill_map:
            role_skill_map[rs.role_id] = []
        role_skill_map[rs.role_id].append(rs.skill_id)

    return jsonify({
        "code": 201,
        "data": role_skill_map
    }), 201
