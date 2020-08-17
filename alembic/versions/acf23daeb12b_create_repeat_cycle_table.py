"""create repeat_cycle table

Revision ID: acf23daeb12b
Revises: f9430ca0c7a5
Create Date: 2020-08-17 18:21:44.217618

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "acf23daeb12b"
down_revision = "f9430ca0c7a5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "repeat_cycles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(20), nullable=False),
    )


def downgrade():
    op.drop_table("repeat_cycles")
