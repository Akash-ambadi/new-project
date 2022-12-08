""""bps_limits"

Revision ID: 9c83d5c18b66
Revises: 2064620faa49
Create Date: 2018-07-17 10:42:22.088675

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9c83d5c18b66'
down_revision = '337366add29d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('max_cbt_get_blocks_bps', sa.Integer(),
                                     nullable=False, default=0))
    op.add_column('agent', sa.Column('max_receiver_bps', sa.Integer(),
                                     nullable=False, default=0))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agent', 'max_receiver_bps')
    op.drop_column('agent', 'max_cbt_get_blocks_bps')
    # ### end Alembic commands ###