"""address table

Revision ID: 7aa41c10d452
Revises: e74b0123a1a2
Create Date: 2022-10-12 19:04:46.580736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aa41c10d452'
down_revision = 'e74b0123a1a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('mobile_number', sa.String(length=11), nullable=True),
    sa.Column('address', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('mobile_number', sa.String(length=11), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'mobile_number')
    op.drop_table('address')
    # ### end Alembic commands ###
