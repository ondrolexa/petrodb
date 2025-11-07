# controllers/customer_controller.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user
from petroapi.database import get_db
from petroapi.models import Profile, ProfileSpot, Project, Sample, User
from petroapi.schema import ProfileSpotCreateSchema, ProfileSpotSchema

router = APIRouter()

# ---------------------------------- PROFILE SPOT


# CREATE Sample Profile Spot
@router.post(
    "/profilespot/{project_id}/{sample_id}/{profile_id}",
    response_model=ProfileSpotSchema,
)
def create_profilespot(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profilespot: ProfileSpotCreateSchema,
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
    if (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile_id)
        .filter_by(index=profilespot.index)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile spot with same index already exists",
        )
    new_profilespot = ProfileSpot(**profilespot.dict())
    profile.spots.append(new_profilespot)
    db.add(profile)
    db.commit()
    db.refresh(new_profilespot)
    return new_profilespot


# CREATE Sample Profile Spot
@router.post(
    "/profilespots/{project_id}/{sample_id}/{profile_id}",
    response_model=list[ProfileSpotSchema],
)
def create_profilespots(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profilespots: list[ProfileSpotCreateSchema],
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
    new_profilespots = []
    for profilespot in profilespots:
        if (
            db.query(ProfileSpot)
            .filter_by(profile_id=profile_id)
            .filter_by(index=profilespot.index)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile spot with same index already exists",
            )
        new_profilespot = ProfileSpot(**profilespot.dict())
        profile.spots.append(new_profilespot)
        new_profilespots.append(new_profilespot)

    db.add(profile)
    db.commit()
    for new_profilespot in new_profilespots:
        db.refresh(new_profilespot)
    return new_profilespots


# READ All Sample Profile Spots
@router.get(
    "/profilespots/{project_id}/{sample_id}/{profile_id}",
    response_model=list[ProfileSpotSchema],
)
def get_profilespots(
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
    profilespots = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile_id)
        .order_by(ProfileSpot.index.asc())
    )
    if profilespots is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spots not found"
        )
    return profilespots


# READ Single Sample Profile Spot
@router.get(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    response_model=ProfileSpotSchema,
)
def get_profilespot(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profilespot_id: int,
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
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile_id)
        .filter_by(id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    return profilespot


# UPDATE Sample Profile
@router.put(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    response_model=ProfileSpotSchema,
)
def update_profilespot(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profilespot_id: int,
    profilespot_update: ProfileSpotCreateSchema,
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
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile_id)
        .filter_by(id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    for field, value in profilespot_update.dict(exclude_unset=True).items():
        setattr(profilespot, field, value)

    db.commit()
    db.refresh(profilespot)
    return profilespot


# DELETE Sample Profile
@router.delete(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    response_model=dict[str, str],
)
def delete_profilespot(
    project_id: int,
    sample_id: int,
    profile_id: int,
    profilespot_id: int,
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
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile_id)
        .filter_by(id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    db.delete(profilespot)
    db.commit()
    return dict(message="Profile spot deleted successfully")
