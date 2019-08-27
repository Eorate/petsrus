"""create pets table

Revision ID: 29a4885791ac
Revises: dac868270418
Create Date: 2019-08-27 16:26:15.198671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "29a4885791ac"
down_revision = "dac868270418"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("species", sa.String(10), nullable=False),
        sa.Column("breed", sa.String(20), nullable=False),
        sa.Column("sex", sa.String(1), nullable=False),
        sa.Column("colour_and_identifying_marks", sa.String(200), nullable=False),
        sa.Column("photo", sa.LargeBinary, nullable=True),
    )


def downgrade():
    op.drop_table("pets")
