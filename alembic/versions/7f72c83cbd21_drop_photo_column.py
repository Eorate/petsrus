"""drop photo column

Revision ID: 7f72c83cbd21
Revises: d15f307412b8
Create Date: 2019-10-19 20:15:44.516313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7f72c83cbd21"
down_revision = "d15f307412b8"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("pets", "photo")


def downgrade():
    op.add_column("pets", sa.Column("photo", sa.LargeBinary, nullable=True))
