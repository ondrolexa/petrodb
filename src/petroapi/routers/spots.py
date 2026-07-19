from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, PageParams, ProjectSample
from petroapi.models import Spot
from petroapi.schema import SpotCreateSchema, SpotSchema

router = APIRouter()

# ---------------------------------- SPOT


# CREATE Sample Spot
@router.post("/spot/{project_id}/{sample_id}", response_model=SpotSchema)
def create_spot(sample: ProjectSample, spot: SpotCreateSchema, db: DB):
    if (
        db.query(Spot)
        .filter_by(sample_id=sample.id)
        .filter_by(label=spot.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spot with same label already exists",
        )
    new_spot = Spot(**spot.model_dump())
    sample.spots.append(new_spot)
    db.add(sample)
    db.commit()
    db.refresh(new_spot)
    return new_spot


# CREATE Sample Spots
@router.post("/spots/{project_id}/{sample_id}", response_model=list[SpotSchema])
def create_spots(sample: ProjectSample, spots: list[SpotCreateSchema], db: DB):
    new_spots = []
    for spot in spots:
        if (
            db.query(Spot)
            .filter_by(sample_id=sample.id)
            .filter_by(label=spot.label)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Spot with label {spot.label} already exists",
            )
        new_spot = Spot(**spot.model_dump())
        sample.spots.append(new_spot)
        new_spots.append(new_spot)

    db.add(sample)
    db.commit()
    for new_spot in new_spots:
        db.refresh(new_spot)
    return new_spots


# READ All Sample Spots
@router.get("/spots/{project_id}/{sample_id}", response_model=list[SpotSchema])
def get_spots(sample: ProjectSample, db: DB, page: PageParams):
    return (
        db.query(Spot)
        .filter_by(sample_id=sample.id)
        .offset(page.offset)
        .limit(page.limit)
    )


# READ Single Sample Spot
@router.get("/spot/{project_id}/{sample_id}/{spot_id}", response_model=SpotSchema)
def get_spot(sample: ProjectSample, spot_id: int, db: DB):
    spot = db.query(Spot).filter_by(sample_id=sample.id, id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    return spot


# UPDATE Sample Spot
@router.put("/spot/{project_id}/{sample_id}/{spot_id}", response_model=SpotSchema)
def update_spot(
    sample: ProjectSample, spot_id: int, spot_update: SpotCreateSchema, db: DB
):
    spot = db.query(Spot).filter_by(sample_id=sample.id, id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    for field, value in spot_update.model_dump(exclude_unset=True).items():
        setattr(spot, field, value)

    db.commit()
    db.refresh(spot)
    return spot


# DELETE Sample Spot
@router.delete(
    "/spot/{project_id}/{sample_id}/{spot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_spot(sample: ProjectSample, spot_id: int, db: DB):
    spot = db.query(Spot).filter_by(sample_id=sample.id, id=spot_id).first()
    if spot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found"
        )
    db.delete(spot)
    db.commit()
