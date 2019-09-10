"""add columns to user table

Revision ID: 99adc1b01c07
Revises: 29a4885791ac
Create Date: 2019-09-08 17:38:38.305354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "99adc1b01c07"
down_revision = "29a4885791ac"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users", sa.Column("email_address", sa.String(50), unique=True, index=True)
    )
    op.add_column("users", sa.Column("telephone", sa.String(20), nullable=True))
    op.add_column("users", sa.Column("country", sa.String(50), nullable=True))


def downgrade():
    op.drop_column("users", "email_address")
    op.drop_column("users", "telephone")
    op.drop_column("users", "country")
