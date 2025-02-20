"""posts table

Revision ID: 3f7f498cd261
Revises: 8d63e432656b
Create Date: 2024-10-11 15:19:00.749377

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3f7f498cd261"
down_revision = "8d63e432656b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.String(length=140), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_post_timestamp"), ["timestamp"], unique=False
        )
        batch_op.create_index(batch_op.f("ix_post_user_id"), ["user_id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("post", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_post_user_id"))
        batch_op.drop_index(batch_op.f("ix_post_timestamp"))

    op.drop_table("post")
    # ### end Alembic commands ###
