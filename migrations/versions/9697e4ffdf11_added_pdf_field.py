"""added pdf field

Revision ID: 9697e4ffdf11
Revises: 1bfd3ceb39a7
Create Date: 2022-10-14 15:45:46.113161

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9697e4ffdf11"
down_revision = "1bfd3ceb39a7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("stationshistory", schema=None) as batch_op:
        batch_op.add_column(sa.Column("pdf", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("stationshistory", schema=None) as batch_op:
        batch_op.drop_column("pdf")

    # ### end Alembic commands ###
