""""device_state_force_full"

Revision ID: 99c21687e80a
Revises: 53cb39787ea5
Create Date: 2018-04-20 13:30:19.308243

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '99c21687e80a'
down_revision = '5b0ba944a6ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_state', sa.Column('force_full', sa.Boolean(),
                                            nullable=False, default=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device_state', 'force_full')
    # ### end Alembic commands ###
