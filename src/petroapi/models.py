from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from petroapi.database import Base

users_projects = Table(
    "users_projects",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "project_id",
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String)
    projects: Mapped[list["Project"]] = relationship(
        secondary=users_projects, back_populates="users", cascade="all, delete"
    )


class Spot(Base):
    __tablename__ = "spots"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_id: Mapped[int] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    mineral: Mapped[str | None] = mapped_column(String)
    values: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)
    sample: Mapped["Sample"] = relationship(back_populates="spots")


class Area(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_id: Mapped[int] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    values: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)
    sample: Mapped["Sample"] = relationship(back_populates="areas")


class ProfileSpot(Base):
    __tablename__ = "profilespots"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    values: Mapped[dict[str, float]] = mapped_column(JSONB, nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="spots")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_id: Mapped[int] = mapped_column(
        ForeignKey("samples.id", ondelete="CASCADE"), nullable=False
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    mineral: Mapped[str] = mapped_column(String, nullable=False)
    spots: Mapped[list[ProfileSpot]] = relationship(
        back_populates="profile", cascade="all, delete"
    )
    sample: Mapped["Sample"] = relationship(back_populates="profiles")


class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String)
    spots: Mapped[list[Spot]] = relationship(
        back_populates="sample", cascade="all, delete"
    )
    areas: Mapped[list[Area]] = relationship(
        back_populates="sample", cascade="all, delete"
    )
    profiles: Mapped[list[Profile]] = relationship(
        back_populates="sample", cascade="all, delete"
    )
    project: Mapped["Project"] = relationship(back_populates="samples")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String)
    samples: Mapped[list[Sample]] = relationship(
        back_populates="project", cascade="all, delete"
    )
    users: Mapped[list[User]] = relationship(
        secondary=users_projects,
        back_populates="projects",
        passive_deletes=True,
    )
