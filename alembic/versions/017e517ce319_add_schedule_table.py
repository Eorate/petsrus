"""Add schedule table

Revision ID: 017e517ce319
Revises: 7f72c83cbd21
Create Date: 2020-04-05 11:21:59.228285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "017e517ce319"
down_revision = "7f72c83cbd21"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pet_id", sa.Integer, sa.ForeignKey("pets.id"), nullable=False),
        sa.Column("date_of_next", sa.Date(), nullable=False),
        sa.Column("repeats", sa.String(3), nullable=False),
        sa.Column("repeat_cycle", sa.String(10), nullable=False),
        sa.Column("schedule_type", sa.String(10), nullable=False),
    )


def downgrade():
    op.drop_table("schedules")
