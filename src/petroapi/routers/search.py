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


@router.get("/search/sample/{project_id}/{sample_name}", response_model=SampleSchema)
def get_sample(project_id: int, sample_name: str, user: CurrentUser, db: DB):
    sample = (
        db.query(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == project_id)
        .filter(Sample.name == sample_name)
        .first()
    )
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    return sample


@router.get("/search/spot/{project_id}/{sample_id}/{label}", response_model=SpotSchema)
def get_spot(project_id: int, sample_id: int, label: str, user: CurrentUser, db: DB):
    spot = (
        db.query(Spot)
        .join(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == project_id)
        .filter(Sample.id == sample_id)
        .filter(Spot.label == label)
        .first()
    )
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    return spot


@router.get(
    "/search/profile/{project_id}/{sample_id}/{label}", response_model=ProfileSchema
)
def get_profile(project_id: int, sample_id: int, label: str, user: CurrentUser, db: DB):
    profile = (
        db.query(Profile)
        .join(Sample)
        .join(Project)
        .where(Project.users.any(id=user.id))
        .filter(Project.id == project_id)
        .filter(Sample.id == sample_id)
        .filter(Profile.label == label)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile
