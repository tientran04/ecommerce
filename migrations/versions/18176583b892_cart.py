"""cart

Revision ID: 18176583b892
Revises: 1cc2c968d42a
Create Date: 2022-10-13 15:50:39.639240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18176583b892'
down_revision = '1cc2c968d42a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_user_id'), 'cart', ['user_id'], unique=False)
    op.create_table('cart_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('address', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('orders', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('orders', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('address', 'customer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_table('cart_items')
    op.drop_index(op.f('ix_cart_user_id'), table_name='cart')
    op.drop_table('cart')
    # ### end Alembic commands ###
