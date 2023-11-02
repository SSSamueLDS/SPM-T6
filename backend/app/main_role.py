#!/usr/bin/env python3
from app import create_app, db
import os

app = create_app()

# Register Blueprints
from . import role
app.register_blueprint(role.role)

def initialize_database():
    with app.app_context():
        db.create_all()

def run_app():
    print("This is flask for " + os.path.basename(__file__) + " role")
    app.run(host='0.0.0.0', port=5005, debug=True)

if __name__ == '__main__':
    initialize_database()
    run_app()