"""change schedules schedule_type column

Revision ID: f9430ca0c7a5
Revises: bd8e47f884b2
Create Date: 2020-08-14 09:38:43.580438

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f9430ca0c7a5"
down_revision = "bd8e47f884b2"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("schedules", "schedule_type")
    op.add_column("schedules", sa.Column("schedule_type", sa.Integer, nullable=True))


def downgrade():
    op.drop_column("schedules", "schedule_type")
    op.add_column("schedules", sa.Column("schedule_type", sa.String(10), nullable=True))
