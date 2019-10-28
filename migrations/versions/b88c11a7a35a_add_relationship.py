"""add relationship

Revision ID: b88c11a7a35a
Revises: 92780e9d1760
Create Date: 2019-10-28 00:05:24.830613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b88c11a7a35a'
down_revision = '92780e9d1760'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'cart', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    # ### end Alembic commands ###