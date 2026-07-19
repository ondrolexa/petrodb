from petroapi.auth import get_password_hash
from petroapi.database import SessionLocal
from petroapi.models import User
from petroapi.settings import get_settings


def init_db():
    settings = get_settings()
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            new_user = User(
                username="admin",
                email=settings.admin_email,
                hashed_password=get_password_hash(settings.admin_password),
                is_admin=True,
            )
            db.add(new_user)
            db.commit()
