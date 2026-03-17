"""create user_progress table

Revision ID: 20261017_0001
Revises:
Create Date: 2026-10-17 00:01:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20261017_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_progress",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("learner_name", sa.String(length=100), nullable=False),
        sa.Column("cefr_level", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_progress_id"), "user_progress", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_progress_id"), table_name="user_progress")
    op.drop_table("user_progress")
