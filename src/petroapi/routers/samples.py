# controllers/customer_controller.py
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from petroapi.models import User, Project, Sample
from petroapi.schema import SampleCreateSchema, SampleSchema
from petroapi.database import get_db
from petroapi.auth import get_current_user

router = APIRouter()

# ---------------------------------- SAMPLE


# CREATE Sample
@router.post("/samples/{project_id}", response_model=SampleSchema)
def create_sample(
    project_id: int,
    sample: SampleCreateSchema,
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
    if db.query(Sample).filter_by(project_id=project_id).filter_by(name=sample.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sample with same name already exists"
        )
    new_sample = Sample(**sample.model_dump())
    project.samples.append(new_sample)
    db.add(project)
    db.commit()
    db.refresh(new_sample)
    return new_sample


# READ All Samples
@router.get("/samples/{project_id}", response_model=list[SampleSchema])
def get_samples(
    project_id: int,
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
    samples = db.query(Sample).filter_by(project_id=project_id)
    if samples is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No samples found"
        )
    return samples


# READ Single Sample
@router.get("/samples/{project_id}/{sample_id}", response_model=SampleSchema)
def get_sample(
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
    return sample


# UPDATE Sample
@router.put("/samples/{project_id}/{sample_id}", response_model=SampleSchema)
def update_sample(
    project_id: int,
    sample_id: int,
    sample_update: SampleCreateSchema,
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
    for field, value in sample_update.model_dump(exclude_unset=True).items():
        setattr(sample, field, value)

    db.commit()
    db.refresh(sample)
    return sample


# DELETE Sample
@router.delete("/samples/{project_id}/{sample_id}", response_model=dict[str, str])
def delete_sample(
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
    db.delete(sample)
    db.commit()
    return dict(message="Sample deleted successfully")
