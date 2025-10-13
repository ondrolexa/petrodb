# controllers/customer_controller.py
import os
from dotenv import load_dotenv
from petroapi.models import User
from petroapi.auth import get_password_hash
from petroapi.database import SessionLocal

_ = load_dotenv()
ADMIN_PASSWORD = str(os.environ.get("ADMIN_PASSWORD"))


def init_db():
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            new_user = User(
                username="admin",
                email=os.environ.get("ADMIN_EMAIL"),
                hashed_password=get_password_hash(ADMIN_PASSWORD),
            )
            db.add(new_user)
            db.commit()
