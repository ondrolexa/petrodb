from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, CurrentUser
from petroapi.models import Profile, Project, Sample, Spot
from petroapi.schema import ProfileSchema, ProjectSchema, SampleSchema, SpotSchema

router = APIRouter()

# ---------------------------------- SEARCH


@router.get("/search/project/{project_name}", response_model=ProjectSchema)
def get_project(project_name: str, user: CurrentUser, db: DB):
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
def get_sample(pid: int, sample_name: str, user: CurrentUser, db: DB):
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


@router.get("/search/spots/{pid}/{sid}/{mineral}", response_model=list[SpotSchema])
def get_spots(pid: int, sid: int, mineral: str, user: CurrentUser, db: DB):
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


@router.get("/search/profile/{pid}/{sid}/{label}", response_model=ProfileSchema)
def get_profile(pid: int, sid: int, label: str, user: CurrentUser, db: DB):
    profile = (
        db.query(Profile)
        .join(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == pid)
        .filter(Sample.id == sid)
        .filter(Profile.label == label)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile
