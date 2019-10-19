"""empty message

Revision ID: ec10ce2fe17c
Revises: 04ee3d9707e2
Create Date: 2019-10-19 06:29:34.227068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec10ce2fe17c'
down_revision = '04ee3d9707e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isVerified', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isVerified')
    # ### end Alembic commands ###