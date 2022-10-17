"""units now use timestamp

Revision ID: d4abd3dd10b7
Revises: 99b64bd599d1
Create Date: 2022-10-17 23:18:38.599604

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d4abd3dd10b7"
down_revision = "99b64bd599d1"
branch_labels = None
depends_on = None

from datetime import datetime


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("units", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created", sa.DateTime(), server_default="", nullable=False)
        )
        batch_op.add_column(sa.Column("updated", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###

    # We want a somewhat useful datetime as not to have parsing errors
    now = datetime.utcnow()
    op.execute(f"UPDATE units SET created = '{now}'")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("units", schema=None) as batch_op:
        batch_op.drop_column("updated")
        batch_op.drop_column("created")

    # ### end Alembic commands ###
