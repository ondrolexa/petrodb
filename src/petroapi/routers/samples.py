from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, OwnedProject, ProjectSample
from petroapi.models import Sample
from petroapi.schema import SampleCreateSchema, SampleSchema

router = APIRouter()

# ---------------------------------- SAMPLE


# CREATE Sample
@router.post("/sample/{project_id}", response_model=SampleSchema)
def create_sample(project: OwnedProject, sample: SampleCreateSchema, db: DB):
    if (
        db.query(Sample)
        .filter_by(project_id=project.id)
        .filter_by(name=sample.name)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sample with same name already exists",
        )
    new_sample = Sample(**sample.model_dump())
    project.samples.append(new_sample)
    db.add(project)
    db.commit()
    db.refresh(new_sample)
    return new_sample


# READ All Samples
@router.get("/samples/{project_id}", response_model=list[SampleSchema])
def get_samples(project: OwnedProject, db: DB):
    return db.query(Sample).filter_by(project_id=project.id)


# READ Single Sample
@router.get("/sample/{project_id}/{sample_id}", response_model=SampleSchema)
def get_sample(sample: ProjectSample):
    return sample


# UPDATE Sample
@router.put("/sample/{project_id}/{sample_id}", response_model=SampleSchema)
def update_sample(sample: ProjectSample, sample_update: SampleCreateSchema, db: DB):
    for field, value in sample_update.model_dump(exclude_unset=True).items():
        setattr(sample, field, value)

    db.commit()
    db.refresh(sample)
    return sample


# DELETE Sample
@router.delete(
    "/sample/{project_id}/{sample_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_sample(sample: ProjectSample, db: DB):
    db.delete(sample)
    db.commit()
