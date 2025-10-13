# controllers/customer_controller.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user, get_password_hash
from petroapi.database import get_db
from petroapi.models import User
from petroapi.schema import UserCreateSchema, UserSchema

router = APIRouter()

# ---------------------------------- AUTH


# Create User
@router.post("/user/", response_model=UserSchema)
def create_user(
    new_user: UserCreateSchema,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id == 1:
        if db.query(User).filter_by(username=new_user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        hashed_password = get_password_hash(new_user.password)
        db_user = User(
            username=new_user.username,
            email=new_user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only administrator can register new user",
            headers={"WWW-Authenticate": "Bearer"},
        )


# READ All Users
@router.get("/users/", response_model=list[UserSchema])
def get_users(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if user.id == 1:
        return db.query(User)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only administrator can list users",
            headers={"WWW-Authenticate": "Bearer"},
        )
