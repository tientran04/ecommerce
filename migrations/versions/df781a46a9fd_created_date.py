"""created date

Revision ID: df781a46a9fd
Revises: f8efa18378ed
Create Date: 2022-10-10 19:50:52.514032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df781a46a9fd'
down_revision = 'f8efa18378ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('created_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'created_date')
    # ### end Alembic commands ###
