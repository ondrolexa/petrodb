from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from petroapi.auth import get_current_user
from petroapi.database import get_db
from petroapi.models import Profile, Project, Sample, User

CurrentUser = Annotated[User, Depends(get_current_user)]
DB = Annotated[Session, Depends(get_db)]


class Pagination:
    def __init__(
        self,
        limit: Annotated[int, Query(le=200)] = 50,
        offset: Annotated[int, Query(ge=0)] = 0,
    ):
        self.limit = limit
        self.offset = offset


PageParams = Annotated[Pagination, Depends()]


def get_owned_project(project_id: int, user: CurrentUser, db: DB) -> Project:
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
    return project


OwnedProject = Annotated[Project, Depends(get_owned_project)]


def get_project_sample(sample_id: int, project: OwnedProject, db: DB) -> Sample:
    sample = db.query(Sample).filter_by(project_id=project.id, id=sample_id).first()
    if sample is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
        )
    return sample


ProjectSample = Annotated[Sample, Depends(get_project_sample)]


def get_sample_profile(profile_id: int, sample: ProjectSample, db: DB) -> Profile:
    profile = db.query(Profile).filter_by(sample_id=sample.id, id=profile_id).first()
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


SampleProfile = Annotated[Profile, Depends(get_sample_profile)]
