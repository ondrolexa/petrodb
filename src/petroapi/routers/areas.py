# controllers/customer_controller.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user
from petroapi.database import get_db
from petroapi.models import Area, Project, Sample, User
from petroapi.schema import AreaCreateSchema, AreaSchema

router = APIRouter()

# ---------------------------------- AREA


# CREATE Sample Area
@router.post("/area/{project_id}/{sample_id}", response_model=AreaSchema)
def create_area(
    project_id: int,
    sample_id: int,
    area: AreaCreateSchema,
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
        db.query(Area)
        .filter_by(sample_id=sample_id)
        .filter_by(label=area.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Area with same label already exists",
        )
    new_area = Area(**area.dict())
    sample.areas.append(new_area)
    db.add(sample)
    db.commit()
    db.refresh(new_area)
    return new_area


# CREATE Sample Areas
@router.post("/areas/{project_id}/{sample_id}", response_model=list[AreaSchema])
def create_areas(
    project_id: int,
    sample_id: int,
    areas: list[AreaCreateSchema],
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
    new_areas = []
    for area in areas:
        if (
            db.query(Area)
            .filter_by(sample_id=sample_id)
            .filter_by(label=area.label)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Area with same label already exists",
            )
        new_area = Area(**area.dict())
        sample.areas.append(new_area)
        new_areas.append(new_area)

    db.add(sample)
    db.commit()
    for new_area in new_areas:
        db.refresh(new_area)
    return new_areas


# READ All Sample Areas
@router.get("/areas/{project_id}/{sample_id}", response_model=list[AreaSchema])
def get_areas(
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
    areas = db.query(Area).filter_by(sample_id=sample_id)
    if areas is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Areas not found"
        )
    return areas


# READ Single Sample Area
@router.get("/area/{project_id}/{sample_id}/{area_id}", response_model=AreaSchema)
def get_area(
    project_id: int,
    sample_id: int,
    area_id: int,
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
    area = db.query(Area).filter_by(sample_id=sample_id).filter_by(id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    return area


# UPDATE Sample Area
@router.put("/area/{project_id}/{sample_id}/{area_id}", response_model=AreaSchema)
def update_area(
    project_id: int,
    sample_id: int,
    area_id: int,
    area_update: AreaCreateSchema,
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
    area = db.query(Area).filter_by(sample_id=sample_id).filter_by(id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    for field, value in area_update.dict(exclude_unset=True).items():
        setattr(area, field, value)

    db.commit()
    db.refresh(area)
    return area


# DELETE Sample Area
@router.delete(
    "/area/{project_id}/{sample_id}/{area_id}", response_model=dict[str, str]
)
def delete_area(
    project_id: int,
    sample_id: int,
    area_id: int,
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
    area = db.query(Area).filter_by(sample_id=sample_id).filter_by(id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    db.delete(area)
    db.commit()
    return dict(message="Area deleted successfully")
