"""create user table

Revision ID: dac868270418
Revises:
Create Date: 2019-08-25 18:17:31.671869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dac868270418"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(32), nullable=False),
        sa.Column("password", sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table("users")
