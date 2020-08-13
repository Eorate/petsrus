"""create schedule_types table

Revision ID: bd8e47f884b2
Revises: eaa6dd3efd84
Create Date: 2020-08-06 13:17:09.824943

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bd8e47f884b2"
down_revision = "eaa6dd3efd84"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "schedule_types",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(20), nullable=False),
    )


def downgrade():
    op.drop_table("schedule_types")
