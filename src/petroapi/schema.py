from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "john",
                "email": "john.doe@email.com",
                "password": "SuperSecret123",
            }
        },
    )

    username: str
    email: EmailStr
    password: str = Field(min_length=12)


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class UserNameSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Mnich",
                "description": "Reconstruction of UHP history",
            }
        },
    )

    name: str
    description: str | None = None


class ProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class SampleCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "SX17W",
                "description": "mylonite",
            }
        },
    )

    name: str
    description: str | None = None


class SampleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class SpotCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
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
        },
    )

    label: str
    mineral: str | None = None
    values: dict[str, float]


class SpotSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    mineral: str | None = None
    values: dict[str, float]


class AreaCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "label": "sp-1",
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
        },
    )

    label: str
    values: dict[str, float]


class AreaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    values: dict[str, float]


class ProfileCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"label": "profile-1", "mineral": "Grt"}},
    )

    label: str
    mineral: str | None = None


class ProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    mineral: str | None = None


class ProfileSpotCreateSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
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
        },
    )

    index: int
    values: dict[str, float]


class ProfileSpotSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    index: int
    values: dict[str, float]
