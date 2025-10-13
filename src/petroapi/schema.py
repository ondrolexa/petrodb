from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john",
                "email": "john.doe@email.com",
                "password": "weakpasword",
            }
        }


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None

    class Config:
        from_attributes = True


class UserNameSchema(BaseModel):
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectCreateSchema(BaseModel):
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Mnich",
                "description": "Reconstruction of UHP history",
            }
        }


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class SampleCreateSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "SX17",
            }
        }


class SampleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SpotCreateSchema(BaseModel):
    label: str
    mineral: str | None = None
    values: dict[str, float]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "label": "pl-1",
                "mineral": "Pl",
                "values": {
                    "SiO2": 65.9,
                    "Al2O3": 19.45,
                    "Fe2O3": 1.03,
                    "CaO": 0.61,
                    "Na2O": 7.12,
                    "K2O": 6.2,
                },
            }
        }


class SpotSchema(BaseModel):
    id: int
    label: str
    mineral: str | None = None
    values: dict[str, float]

    class Config:
        from_attributes = True


class AreaCreateSchema(BaseModel):
    label: str
    weight: float
    values: dict[str, float]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "label": "sp-1",
                "weight": 1,
                "values": {
                    "Na2O": 4.891811,
                    "MgO": 0.254737,
                    "Al2O3": 14.71383,
                    "SiO2": 64.95177,
                    "K2O": 1.915395,
                    "CaO": 1.360331,
                    "TiO2": 0.1688591,
                    "MnO": 0.03100058,
                    "FeO": 1.413152,
                },
            }
        }


class AreaSchema(BaseModel):
    id: int
    label: str
    weight: float
    values: dict[str, float]

    class Config:
        from_attributes = True


class ProfileCreateSchema(BaseModel):
    label: str
    mineral: str | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"label": "profile-1", "mineral": "Grt"}}


class ProfileSchema(BaseModel):
    id: int
    label: str
    mineral: str | None = None

    class Config:
        from_attributes = True


class ProfileSpotCreateSchema(BaseModel):
    index: int
    values: dict[str, float]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "index": 6,
                "values": {
                    "Na2O": 0.052,
                    "P2O5": 0.061,
                    "Al2O3": 21.077,
                    "CaO": 10.325,
                    "FeO": 28.608,
                    "MnO": 0.945,
                    "TiO2": 0.07,
                    "SiO2": 38.071,
                    "MgO": 1.033,
                },
            }
        }


class ProfileSpotSchema(BaseModel):
    id: int
    index: int
    values: dict[str, float]

    class Config:
        from_attributes = True
