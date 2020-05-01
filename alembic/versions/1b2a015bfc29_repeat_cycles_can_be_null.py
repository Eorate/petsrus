"""repeat_cycle can be null

Revision ID: 1b2a015bfc29
Revises: 017e517ce319
Create Date: 2020-04-30 13:54:06.535877

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1b2a015bfc29"
down_revision = "017e517ce319"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "schedules", "repeat_cycle", existing_type=sa.String(10), nullable=True
    )


def downgrade():
    op.alter_column(
        "schedules", "repeat_cycle", existing_type=sa.String(10), nullable=False
    )
