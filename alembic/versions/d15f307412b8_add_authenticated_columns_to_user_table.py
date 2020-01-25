"""add authenticated columns to user table

Revision ID: d15f307412b8
Revises: 99adc1b01c07
Create Date: 2019-10-13 17:37:59.888514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d15f307412b8"
down_revision = "99adc1b01c07"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("authenticated", sa.Boolean, default=False))


def downgrade():
    op.drop_column("users", "authenticated")
