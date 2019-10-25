"""add price column

Revision ID: 518183cf2917
Revises: 32afacfb9e08
Create Date: 2019-10-21 19:53:29.113984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '518183cf2917'
down_revision = '32afacfb9e08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('price', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'price')
    # ### end Alembic commands ###