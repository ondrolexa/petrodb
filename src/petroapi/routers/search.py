# controllers/customer_controller.py
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from petroapi.models import User, Project, Sample, Spot
from petroapi.schema import (
    ProjectSchema,
    SampleSchema,
    SpotSchema,
)
from petroapi.database import get_db
from petroapi.auth import get_current_user

router = APIRouter()

# ---------------------------------- SEARCH


@router.get("/search/project/{project_name}", response_model=ProjectSchema)
def get_project(
    project_name: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    project = (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(name=project_name)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


@router.get("/search/sample/{pid}/{sample_name}", response_model=SampleSchema)
def get_sample(
    pid: int,
    sample_name: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    sample = (
        db.query(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == pid)
        .filter(Sample.name == sample_name)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    return sample


@router.get("/search/spot/{pid}/{sid}/{mineral}", response_model=list[SpotSchema])
def get_spot(
    pid: int,
    sid: int,
    mineral: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    spots = (
        db.query(Spot)
        .join(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == pid)
        .filter(Sample.id == sid)
        .filter(Spot.mineral == mineral)
        .all()
    )
    if not spots:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mineral not found"
        )
    return spots
