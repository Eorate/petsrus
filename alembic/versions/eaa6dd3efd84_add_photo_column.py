"""add photo column

Revision ID: eaa6dd3efd84
Revises: 1b2a015bfc29
Create Date: 2020-05-11 10:26:41.717877

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eaa6dd3efd84"
down_revision = "1b2a015bfc29"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "pets", sa.Column("photo", sa.Text, nullable=True, default="default.png")
    )


def downgrade():
    op.drop_column("pets", "photo")
