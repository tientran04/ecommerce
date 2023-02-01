"""orders table

Revision ID: 9fc9c5c504b5
Revises: f167cf86726a
Create Date: 2022-10-13 08:54:34.632760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fc9c5c504b5'
down_revision = 'f167cf86726a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('mobile_number', sa.String(length=15), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=True)
    op.create_index(op.f('ix_customers_first_name'), 'customers', ['first_name'], unique=False)
    op.create_index(op.f('ix_customers_last_name'), 'customers', ['last_name'], unique=False)
    op.create_table('order_status',
    sa.Column('id', sa.String(length=1), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('shipping_address_id', sa.Integer(), nullable=False),
    sa.Column('billing_address_id', sa.Integer(), nullable=False),
    sa.Column('total_items', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['billing_address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['shipping_address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['status'], ['order_status.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_billing_address_id'), 'orders', ['billing_address_id'], unique=False)
    op.create_index(op.f('ix_orders_customer_id'), 'orders', ['customer_id'], unique=False)
    op.create_index(op.f('ix_orders_order_date'), 'orders', ['order_date'], unique=False)
    op.create_index(op.f('ix_orders_shipping_address_id'), 'orders', ['shipping_address_id'], unique=False)
    op.create_table('order_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=60), nullable=True),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.Column('order_quantity', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_details_order_date'), 'order_details', ['order_date'], unique=False)
    op.create_index(op.f('ix_order_details_order_id'), 'order_details', ['order_id'], unique=False)
    op.create_index(op.f('ix_order_details_product_id'), 'order_details', ['product_id'], unique=False)
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_table('users')
    op.add_column('address', sa.Column('customer_id', sa.Integer(), nullable=False))
    op.drop_index('ix_address_user_id', table_name='address')
    op.create_index(op.f('ix_address_customer_id'), 'address', ['customer_id'], unique=False)
    op.drop_constraint('address_user_id_fkey', 'address', type_='foreignkey')
    op.create_foreign_key(None, 'address', 'customers', ['customer_id'], ['id'])
    op.drop_column('address', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('address', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'address', type_='foreignkey')
    op.create_foreign_key('address_user_id_fkey', 'address', 'users', ['user_id'], ['id'])
    op.drop_index(op.f('ix_address_customer_id'), table_name='address')
    op.create_index('ix_address_user_id', 'address', ['user_id'], unique=False)
    op.drop_column('address', 'customer_id')
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('mobile_number', sa.VARCHAR(length=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.drop_index(op.f('ix_order_details_product_id'), table_name='order_details')
    op.drop_index(op.f('ix_order_details_order_id'), table_name='order_details')
    op.drop_index(op.f('ix_order_details_order_date'), table_name='order_details')
    op.drop_table('order_details')
    op.drop_index(op.f('ix_orders_shipping_address_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_order_date'), table_name='orders')
    op.drop_index(op.f('ix_orders_customer_id'), table_name='orders')
    op.drop_index(op.f('ix_orders_billing_address_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_table('order_status')
    op.drop_index(op.f('ix_customers_last_name'), table_name='customers')
    op.drop_index(op.f('ix_customers_first_name'), table_name='customers')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
    # ### end Alembic commands ###