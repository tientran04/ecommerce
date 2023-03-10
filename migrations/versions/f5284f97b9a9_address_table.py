"""address table

Revision ID: f5284f97b9a9
Revises: 7aa41c10d452
Create Date: 2022-10-12 19:32:46.139759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5284f97b9a9'
down_revision = '7aa41c10d452'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_address_first_name'), 'address', ['first_name'], unique=False)
    op.create_index(op.f('ix_address_last_name'), 'address', ['last_name'], unique=False)
    op.create_index(op.f('ix_address_mobile_number'), 'address', ['mobile_number'], unique=False)
    op.create_index(op.f('ix_address_user_id'), 'address', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_address_user_id'), table_name='address')
    op.drop_index(op.f('ix_address_mobile_number'), table_name='address')
    op.drop_index(op.f('ix_address_last_name'), table_name='address')
    op.drop_index(op.f('ix_address_first_name'), table_name='address')
    op.drop_column('address', 'user_id')
    # ### end Alembic commands ###
