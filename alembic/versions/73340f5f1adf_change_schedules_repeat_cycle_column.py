"""change_schedules_repeat_cycle_column

Revision ID: 73340f5f1adf
Revises: acf23daeb12b
Create Date: 2020-08-23 12:09:49.948494

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "73340f5f1adf"
down_revision = "acf23daeb12b"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("schedules", "repeat_cycle")
    op.add_column("schedules", sa.Column("repeat_cycle", sa.Integer, nullable=True))


def downgrade():
    op.drop_column("schedules", "repeat_cycle")
    op.add_column("schedules", sa.Column("repeat_cycle", sa.String(10), nullable=True))
