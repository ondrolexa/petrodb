from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, PageParams, SampleProfile
from petroapi.models import ProfileSpot
from petroapi.schema import ProfileSpotCreateSchema, ProfileSpotSchema

router = APIRouter()

# ---------------------------------- PROFILE SPOT


# CREATE Sample Profile Spot
@router.post(
    "/profilespot/{project_id}/{sample_id}/{profile_id}",
    response_model=ProfileSpotSchema,
)
def create_profilespot(
    profile: SampleProfile, profilespot: ProfileSpotCreateSchema, db: DB
):
    if (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile.id)
        .filter_by(index=profilespot.index)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile spot with same index already exists",
        )
    new_profilespot = ProfileSpot(**profilespot.model_dump())
    profile.spots.append(new_profilespot)
    db.add(profile)
    db.commit()
    db.refresh(new_profilespot)
    return new_profilespot


# CREATE Sample Profile Spots
@router.post(
    "/profilespots/{project_id}/{sample_id}/{profile_id}",
    response_model=list[ProfileSpotSchema],
)
def create_profilespots(
    profile: SampleProfile, profilespots: list[ProfileSpotCreateSchema], db: DB
):
    new_profilespots = []
    for profilespot in profilespots:
        if (
            db.query(ProfileSpot)
            .filter_by(profile_id=profile.id)
            .filter_by(index=profilespot.index)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile spot with same index already exists",
            )
        new_profilespot = ProfileSpot(**profilespot.model_dump())
        profile.spots.append(new_profilespot)
        new_profilespots.append(new_profilespot)

    db.add(profile)
    db.commit()
    for new_profilespot in new_profilespots:
        db.refresh(new_profilespot)
    return new_profilespots


# READ All Sample Profile Spots
@router.get(
    "/profilespots/{project_id}/{sample_id}/{profile_id}",
    response_model=list[ProfileSpotSchema],
)
def get_profilespots(profile: SampleProfile, db: DB, page: PageParams):
    return (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile.id)
        .order_by(ProfileSpot.index.asc())
        .offset(page.offset)
        .limit(page.limit)
    )


# READ Single Sample Profile Spot
@router.get(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    response_model=ProfileSpotSchema,
)
def get_profilespot(profile: SampleProfile, profilespot_id: int, db: DB):
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile.id, id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    return profilespot


# UPDATE Sample Profile Spot
@router.put(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    response_model=ProfileSpotSchema,
)
def update_profilespot(
    profile: SampleProfile,
    profilespot_id: int,
    profilespot_update: ProfileSpotCreateSchema,
    db: DB,
):
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile.id, id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    for field, value in profilespot_update.model_dump(exclude_unset=True).items():
        setattr(profilespot, field, value)

    db.commit()
    db.refresh(profilespot)
    return profilespot


# DELETE Sample Profile Spot
@router.delete(
    "/profilespot/{project_id}/{sample_id}/{profile_id}/{profilespot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_profilespot(profile: SampleProfile, profilespot_id: int, db: DB):
    profilespot = (
        db.query(ProfileSpot)
        .filter_by(profile_id=profile.id, id=profilespot_id)
        .first()
    )
    if profilespot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile spot not found"
        )
    db.delete(profilespot)
    db.commit()
