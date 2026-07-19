from fastapi import APIRouter, HTTPException, status

from petroapi.auth import get_password_hash
from petroapi.deps import DB, CurrentUser, PageParams
from petroapi.models import User
from petroapi.schema import UserCreateSchema, UserSchema

router = APIRouter()

# ---------------------------------- AUTH


# Create User
@router.post("/user/", response_model=UserSchema)
def create_user(new_user: UserCreateSchema, user: CurrentUser, db: DB):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only administrator can register new user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db.query(User).filter_by(username=new_user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    db_user = User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ All Users
@router.get("/users/", response_model=list[UserSchema])
def get_users(user: CurrentUser, db: DB, page: PageParams):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only administrator can list users",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db.query(User).offset(page.offset).limit(page.limit)
