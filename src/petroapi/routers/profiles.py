from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, PageParams, ProjectSample, SampleProfile
from petroapi.models import Profile
from petroapi.schema import ProfileCreateSchema, ProfileSchema

router = APIRouter()

# ---------------------------------- PROFILE


# CREATE Sample Profile
@router.post("/profile/{project_id}/{sample_id}", response_model=ProfileSchema)
def create_profile(sample: ProjectSample, profile: ProfileCreateSchema, db: DB):
    if (
        db.query(Profile)
        .filter_by(sample_id=sample.id)
        .filter_by(label=profile.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile with same label already exists",
        )
    new_profile = Profile(**profile.model_dump())
    sample.profiles.append(new_profile)
    db.add(sample)
    db.commit()
    db.refresh(new_profile)
    return new_profile


# READ All Sample Profiles
@router.get("/profiles/{project_id}/{sample_id}", response_model=list[ProfileSchema])
def get_profiles(sample: ProjectSample, db: DB, page: PageParams):
    return (
        db.query(Profile)
        .filter_by(sample_id=sample.id)
        .offset(page.offset)
        .limit(page.limit)
    )


# READ Single Sample Profile
@router.get(
    "/profile/{project_id}/{sample_id}/{profile_id}", response_model=ProfileSchema
)
def get_profile(profile: SampleProfile):
    return profile


# UPDATE Sample Profile
@router.put(
    "/profile/{project_id}/{sample_id}/{profile_id}",
    response_model=ProfileSchema,
)
def update_profile(profile: SampleProfile, profile_update: ProfileCreateSchema, db: DB):
    for field, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


# DELETE Sample Profile
@router.delete(
    "/profile/{project_id}/{sample_id}/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profile(profile: SampleProfile, db: DB):
    db.delete(profile)
    db.commit()
