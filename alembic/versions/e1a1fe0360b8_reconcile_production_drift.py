"""reconcile production drift

Revision ID: e1a1fe0360b8
Revises: a2a17f918abd
Create Date: 2026-07-19 14:06:47.980023

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1a1fe0360b8"
down_revision: Union[str, Sequence[str], None] = "a2a17f918abd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "areas_sample_id_label_key", "areas", ["sample_id", "label"]
    )
    op.create_unique_constraint(
        "profiles_sample_id_label_key", "profiles", ["sample_id", "label"]
    )
    op.create_unique_constraint(
        "profilespots_profile_id_index_key", "profilespots", ["profile_id", "index"]
    )
    op.create_unique_constraint(
        "samples_project_id_name_key", "samples", ["project_id", "name"]
    )
    op.create_unique_constraint(
        "spots_sample_id_label_key", "spots", ["sample_id", "label"]
    )
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column("users", "is_admin", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_admin")
    op.drop_constraint("spots_sample_id_label_key", "spots", type_="unique")
    op.drop_constraint("samples_project_id_name_key", "samples", type_="unique")
    op.drop_constraint(
        "profilespots_profile_id_index_key", "profilespots", type_="unique"
    )
    op.drop_constraint("profiles_sample_id_label_key", "profiles", type_="unique")
    op.drop_constraint("areas_sample_id_label_key", "areas", type_="unique")
