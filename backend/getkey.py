import os
from dotenv import load_dotenv

load_dotenv()

db_key= os.getenv("db_key")
db_password = os.environ.get("db_password")
