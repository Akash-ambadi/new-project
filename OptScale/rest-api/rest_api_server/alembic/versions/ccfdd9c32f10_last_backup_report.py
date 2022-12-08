""""last_backup_report"

Revision ID: ccfdd9c32f10
Revises: b532c6a989db
Create Date: 2018-12-27 16:47:56.985269

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ccfdd9c32f10'
down_revision = '82532f479b05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_state', sa.Column('last_backup_report', sa.Integer(),
                                            nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device_state', 'last_backup_report')
    # ### end Alembic commands ###
