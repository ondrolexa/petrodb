from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, CurrentUser, OwnedProject
from petroapi.models import Project, User
from petroapi.schema import ProjectCreateSchema, ProjectSchema, UserNameSchema

router = APIRouter()

# ---------------------------------- PROJECT


# CREATE Project
@router.post("/project/", response_model=ProjectSchema)
def create_project(project: ProjectCreateSchema, user: CurrentUser, db: DB):
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
def get_projects(user: CurrentUser, db: DB):
    return db.query(Project).where(Project.users.any(id=user.id))


# READ Single Project
@router.get("/project/{project_id}", response_model=ProjectSchema)
def get_project(project: OwnedProject):
    return project


# UPDATE Project
@router.put("/project/{project_id}", response_model=ProjectSchema)
def update_project(project: OwnedProject, project_update: ProjectCreateSchema, db: DB):
    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return project


# ADD USER Project
@router.put("/project/{project_id}/adduser", response_model=ProjectSchema)
def adduser_project(project: OwnedProject, user_update: UserNameSchema, db: DB):
    new_user = db.query(User).filter_by(username=user_update.username).first()
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if new_user in project.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already in project",
        )
    project.users.append(new_user)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


# REMOVE USER Project
@router.put("/project/{project_id}/removeuser", response_model=ProjectSchema)
def removeuser_project(
    project: OwnedProject, user_update: UserNameSchema, user: CurrentUser, db: DB
):
    user_todel = db.query(User).filter_by(username=user_update.username).first()
    if user_todel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_todel.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot remove yourself",
        )
    if user_todel not in project.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not in project",
        )
    project.users.remove(user_todel)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


# DELETE Project
@router.delete("/project/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project: OwnedProject, db: DB):
    db.delete(project)
    db.commit()
