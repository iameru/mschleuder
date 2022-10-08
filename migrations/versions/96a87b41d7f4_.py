"""empty message

Revision ID: 96a87b41d7f4
Revises:
Create Date: 2022-10-08 11:39:03.968308

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "96a87b41d7f4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "distribution",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("in_progress", sa.Boolean(), nullable=False),
        sa.Column("finalized", sa.Boolean(), nullable=True),
        sa.Column("date_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "products",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("info", sa.String(length=128), nullable=True),
        sa.Column("last_distribution", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("info", sa.String(length=128), nullable=True),
        sa.Column("header", sa.String(length=128), nullable=True),
        sa.Column("footer", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("display_name"),
        sa.UniqueConstraint("footer"),
        sa.UniqueConstraint("header"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "stations",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("info", sa.String(length=128), nullable=True),
        sa.Column("delivery_order", sa.Integer(), nullable=False),
        sa.Column("members_full", sa.Integer(), nullable=False),
        sa.Column("members_half", sa.Integer(), nullable=False),
        sa.Column(
            "members_total",
            sa.Integer(),
            sa.Computed(
                "members_full + members_half",
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "units",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("by_piece", sa.Boolean(), nullable=False),
        sa.Column("shortname", sa.String(length=128), nullable=False),
        sa.Column("longname", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("longname"),
        sa.UniqueConstraint("shortname"),
    )
    op.create_table(
        "product_units",
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
        ),
        sa.PrimaryKeyConstraint("unit_id", "product_id"),
    )
    op.create_table(
        "stationshistory",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("info", sa.String(length=128), nullable=True),
        sa.Column("delivery_order", sa.Integer(), nullable=False),
        sa.Column("members_full", sa.Integer(), nullable=False),
        sa.Column("members_half", sa.Integer(), nullable=False),
        sa.Column("members_total", sa.Integer(), nullable=False),
        sa.Column("time_archived", sa.DateTime(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("distribution_id", sa.Integer(), nullable=False),
        sa.Column("station_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["distribution_id"],
            ["distribution.id"],
        ),
        sa.ForeignKeyConstraint(
            ["station_id"],
            ["stations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "share",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("stationhistory_id", sa.Integer(), nullable=False),
        sa.Column("distribution_id", sa.Integer(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("single_full", sa.Float(precision=8, asdecimal=True), nullable=True),
        sa.Column("single_half", sa.Float(precision=8, asdecimal=True), nullable=True),
        sa.Column(
            "single_total",
            sa.Float(),
            sa.Computed(
                "single_full + single_half",
            ),
            nullable=True,
        ),
        sa.Column("sum_full", sa.Float(precision=8, asdecimal=True), nullable=True),
        sa.Column("sum_half", sa.Float(precision=8, asdecimal=True), nullable=True),
        sa.Column(
            "sum_total",
            sa.Float(),
            sa.Computed(
                "sum_full + sum_half",
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["distribution_id"],
            ["distribution.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["stationhistory_id"],
            ["stationshistory.id"],
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("share")
    op.drop_table("stationshistory")
    op.drop_table("product_units")
    op.drop_table("units")
    op.drop_table("stations")
    op.drop_table("settings")
    op.drop_table("products")
    op.drop_table("distribution")
    # ### end Alembic commands ###