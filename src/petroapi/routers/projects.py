# controllers/customer_controller.py
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from petroapi.models import User, Project
from petroapi.schema import ProjectCreateSchema, ProjectSchema, UserNameSchema
from petroapi.database import get_db
from petroapi.auth import get_current_user

router = APIRouter()

# ---------------------------------- PROJECT


# CREATE Project
@router.post("/projects/", response_model=ProjectSchema)
def create_project(
    project: ProjectCreateSchema,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    if (
        db.query(Project)
        .where(Project.users.any(id=user.id))
        .filter_by(name=project.name)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with same name already exists",
        )

    new_project = Project(**project.model_dump(), users=[user])
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# READ All Projects
@router.get("/projects/", response_model=list[ProjectSchema])
def get_projects(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    # return user.projects
    return db.query(Project).where(Project.users.any(id=user.id))


# READ Single Project
@router.get("/projects/{project_id}", response_model=ProjectSchema)
def get_project(
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
    return project


# UPDATE Project
@router.put("/projects/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    project_update: ProjectCreateSchema,
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
    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


# ADD USER Project
@router.put("/projects/{project_id}/adduser", response_model=ProjectSchema)
def adduser_project(
    project_id: int,
    user_update: UserNameSchema,
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
    new_user = db.query(User).filter_by(username=user_update.username).first()
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if new_user.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already there",
        )
    if new_user not in project.users:
        project.users.append(new_user)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in project",
        )


# ADD USER Project
@router.put("/projects/{project_id}/removeuser", response_model=ProjectSchema)
def removeuser_project(
    project_id: int,
    user_update: UserNameSchema,
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
    new_user = db.query(User).filter_by(username=user_update.username).first()
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if new_user.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot remove yourself",
        )
    if new_user in project.users:
        project.users.remove(user)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not in project",
        )


# DELETE Project
@router.delete("/projects/{project_id}", response_model=dict[str, str])
def delete_project(
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
    db.delete(project)
    db.commit()
    return dict(message="Project deleted successfully")
