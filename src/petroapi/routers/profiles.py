# controllers/customer_controller.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user
from petroapi.database import get_db
from petroapi.models import Profile, Project, Sample, User
from petroapi.schema import ProfileCreateSchema, ProfileSchema

router = APIRouter()

# ---------------------------------- PROFILE


# CREATE Sample Profile
@router.post("/profile/{project_id}/{sample_id}", response_model=ProfileSchema)
def create_profile(
    project_id: int,
    sample_id: int,
    profile: ProfileCreateSchema,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(id=project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    sample = (
        db.query(Sample)
        .filter_by(project_id=project_id)
        .filter_by(id=sample_id)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    if (
        db.query(Profile)
        .filter_by(sample_id=sample_id)
        .filter_by(label=profile.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile with same label already exists",
        )
    new_profile = Profile(**profile.dict())
    sample.profiles.append(new_profile)
    db.add(sample)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# READ All Sample Profiles
@router.get("/profiles/{project_id}/{sample_id}", response_model=list[ProfileSchema])
def get_profiles(
    project_id: int,
    sample_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(id=project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    sample = (
        db.query(Sample)
        .filter_by(project_id=project_id)
        .filter_by(id=sample_id)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    profiles = db.query(Profile).filter_by(sample_id=sample_id)
    if profiles is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profiles not found"
        )
    return profiles


# READ Single Sample Profile
@router.get(
    "/profile/{project_id}/{sample_id}/{profile_id}", response_model=ProfileSchema
)
def get_profile(
    project_id: int,
    sample_id: int,
    profile_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(id=project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    sample = (
        db.query(Sample)
        .filter_by(project_id=project_id)
        .filter_by(id=sample_id)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    profile = (
        db.query(Profile)
        .filter_by(sample_id=sample_id)
        .filter_by(id=profile_id)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


# UPDATE Sample Profile
@router.put(
    "/profile/{project_id}/{sample_id}/{profile_id}",
    response_model=ProfileSchema,
)
def update_profile(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profile_update: ProfileCreateSchema,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(id=project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    sample = (
        db.query(Sample)
        .filter_by(project_id=project_id)
        .filter_by(id=sample_id)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    profile = (
        db.query(Profile)
        .filter_by(sample_id=sample_id)
        .filter_by(id=profile_id)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    for field, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


# DELETE Sample Profile
@router.delete(
    "/profile/{project_id}/{sample_id}/{profile_id}",
    response_model=dict[str, str],
)
def delete_profile(
    project_id: int,
    sample_id: int,
    profile_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(id=project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    sample = (
        db.query(Sample)
        .filter_by(project_id=project_id)
        .filter_by(id=sample_id)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    profile = (
        db.query(Profile)
        .filter_by(sample_id=sample_id)
        .filter_by(id=profile_id)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    db.delete(profile)
    db.commit()
    return dict(message="Profile deleted successfully")
