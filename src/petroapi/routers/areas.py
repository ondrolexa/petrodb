from fastapi import APIRouter, HTTPException, status

from petroapi.deps import DB, PageParams, ProjectSample
from petroapi.models import Area
from petroapi.schema import AreaCreateSchema, AreaSchema

router = APIRouter()

# ---------------------------------- AREA


# CREATE Sample Area
@router.post("/area/{project_id}/{sample_id}", response_model=AreaSchema)
def create_area(sample: ProjectSample, area: AreaCreateSchema, db: DB):
    if (
        db.query(Area)
        .filter_by(sample_id=sample.id)
        .filter_by(label=area.label)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Area with same label already exists",
        )
    new_area = Area(**area.model_dump())
    sample.areas.append(new_area)
    db.add(sample)
    db.commit()
    db.refresh(new_area)
    return new_area


# CREATE Sample Areas
@router.post("/areas/{project_id}/{sample_id}", response_model=list[AreaSchema])
def create_areas(sample: ProjectSample, areas: list[AreaCreateSchema], db: DB):
    new_areas = []
    for area in areas:
        if (
            db.query(Area)
            .filter_by(sample_id=sample.id)
            .filter_by(label=area.label)
            .first()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Area with same label already exists",
            )
        new_area = Area(**area.model_dump())
        sample.areas.append(new_area)
        new_areas.append(new_area)

    db.add(sample)
    db.commit()
    for new_area in new_areas:
        db.refresh(new_area)
    return new_areas


# READ All Sample Areas
@router.get("/areas/{project_id}/{sample_id}", response_model=list[AreaSchema])
def get_areas(sample: ProjectSample, db: DB, page: PageParams):
    return (
        db.query(Area)
        .filter_by(sample_id=sample.id)
        .offset(page.offset)
        .limit(page.limit)
    )


# READ Single Sample Area
@router.get("/area/{project_id}/{sample_id}/{area_id}", response_model=AreaSchema)
def get_area(sample: ProjectSample, area_id: int, db: DB):
    area = db.query(Area).filter_by(sample_id=sample.id, id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    return area


# UPDATE Sample Area
@router.put("/area/{project_id}/{sample_id}/{area_id}", response_model=AreaSchema)
def update_area(
    sample: ProjectSample, area_id: int, area_update: AreaCreateSchema, db: DB
):
    area = db.query(Area).filter_by(sample_id=sample.id, id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    for field, value in area_update.model_dump(exclude_unset=True).items():
        setattr(area, field, value)

    db.commit()
    db.refresh(area)
    return area


# DELETE Sample Area
@router.delete(
    "/area/{project_id}/{sample_id}/{area_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_area(sample: ProjectSample, area_id: int, db: DB):
    area = db.query(Area).filter_by(sample_id=sample.id, id=area_id).first()
    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found"
        )
    db.delete(area)
    db.commit()
