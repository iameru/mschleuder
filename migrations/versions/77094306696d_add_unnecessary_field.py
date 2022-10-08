"""add_unnecessary_field

Revision ID: 77094306696d
Revises: 96a87b41d7f4
Create Date: 2022-10-08 15:00:10.804984

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "77094306696d"
down_revision = "96a87b41d7f4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "products",
        sa.Column(
            "unnecessary_field_to_try_out_migrations", sa.Integer(), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("products", "unnecessary_field_to_try_out_migrations")
    # ### end Alembic commands ###
