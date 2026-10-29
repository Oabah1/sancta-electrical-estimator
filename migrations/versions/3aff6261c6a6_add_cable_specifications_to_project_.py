"""Add cable specifications to project estimates."""

from alembic import op
import sqlalchemy as sa


revision = "3aff6261c6a6"
down_revision = "03782e068b42"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("project_cable_estimate") as batch_op:
        batch_op.add_column(
            sa.Column("conductor_material", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(
            sa.Column("insulation", sa.String(length=100), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("project_cable_estimate") as batch_op:
        batch_op.drop_column("insulation")
        batch_op.drop_column("conductor_material")
