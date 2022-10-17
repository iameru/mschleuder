"""remove unused fields

Revision ID: 99b64bd599d1
Revises: 9697e4ffdf11
Create Date: 2022-10-14 18:18:01.229305

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "99b64bd599d1"
down_revision = "9697e4ffdf11"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("settings", schema=None) as batch_op:
        batch_op.drop_column("display_name")
        batch_op.drop_column("header")
        batch_op.drop_column("info")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("settings", schema=None) as batch_op:
        batch_op.add_column(sa.Column("info", sa.VARCHAR(length=128), nullable=True))
        batch_op.add_column(sa.Column("header", sa.VARCHAR(length=128), nullable=True))
        batch_op.add_column(
            sa.Column("display_name", sa.VARCHAR(length=128), nullable=False)
        )

    # ### end Alembic commands ###