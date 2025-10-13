# controllers/customer_controller.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user
from petroapi.database import get_db
from petroapi.models import Project, Sample, Spot, User
from petroapi.schema import SpotCreateSchema, SpotSchema

router = APIRouter()

# ---------------------------------- SPOT


# CREATE Sample Spot
@router.post("/spot/{project_id}/{sample_id}", response_model=SpotSchema)
def create_spot(
    project_id: int,
    sample_id: int,
    spot: SpotCreateSchema,
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
        db.query(Spot)
        .filter_by(sample_id=sample_id)
        .filter_by(label=spot.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spot with same label already exists",
        )
    new_spot = Spot(**spot.dict())
    sample.spots.append(new_spot)
    db.add(sample)
    db.commit()
    db.refresh(new_spot)
    return new_spot


# CREATE Sample Spots
@router.post("/spots/{project_id}/{sample_id}", response_model=list[SpotSchema])
def create_spots(
    project_id: int,
    sample_id: int,
    spots: list[SpotCreateSchema],
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
    new_spots = []
    for spot in spots:
        if (
            db.query(Spot)
            .filter_by(sample_id=sample_id)
            .filter_by(label=spot.label)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Spot with label {spot.label} already exists",
            )
        new_spot = Spot(**spot.dict())
        sample.spots.append(new_spot)
        new_spots.append(new_spot)

    db.add(sample)
    db.commit()
    for new_spot in new_spots:
        db.refresh(new_spot)
    return new_spots


# READ All Sample Spots
@router.get("/spots/{project_id}/{sample_id}", response_model=list[SpotSchema])
def get_spots(
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
    spots = db.query(Spot).filter_by(sample_id=sample_id)
    if spots is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spots not found"
        )
    return spots


# READ Single Sample Spot
@router.get("/spot/{project_id}/{sample_id}/{spot_id}")
def get_spot(
    project_id: int,
    sample_id: int,
    spot_id: int,
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
    spot = db.query(Spot).filter_by(sample_id=sample_id).filter_by(id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    return spot


# UPDATE Sample Spot
@router.put("/spot/{project_id}/{sample_id}/{spot_id}", response_model=SpotSchema)
def update_spot(
    project_id: int,
    sample_id: int,
    spot_id: int,
    spot_update: SpotCreateSchema,
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
    spot = db.query(Spot).filter_by(sample_id=sample_id).filter_by(id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    for field, value in spot_update.dict(exclude_unset=True).items():
        setattr(spot, field, value)

    db.commit()
    db.refresh(spot)
    return spot


# DELETE Sample Spot
@router.delete(
    "/spot/{project_id}/{sample_id}/{spot_id}", response_model=dict[str, str]
)
def delete_spot(
    project_id: int,
    sample_id: int,
    spot_id: int,
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
    spot = db.query(Spot).filter_by(sample_id=sample_id).filter_by(id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    db.delete(spot)
    db.commit()
    return dict(message="Spot deleted successfully")
