""""“device_sync_statuses”"

Revision ID: ee0476ed5da2
Revises: 86a9064bd530
Create Date: 2017-10-30 14:00:11.091227

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee0476ed5da2'
down_revision = '86a9064bd530'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('failback', sa.Column('progress', sa.Integer(),
                                        nullable=False))
    op.add_column('failback_device', sa.Column('progress', sa.Integer(),
                                               nullable=False))
    op.alter_column('failback_device', 'sync_status',
                    existing_type=sa.Enum('IDLE', 'SYNC', 'READY', 'ERROR'),
                    nullable=False)
    op.alter_column('failback', 'state',
                    existing_type=sa.Enum('INCOMPLETE', 'IDLE', 'READY',
                                          'RUNNING', 'SYNCHRONIZED', 'ERROR'),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('failback_device', 'progress')
    op.drop_column('failback', 'progress')
    op.alter_column('failback_device', 'sync_status', existing_type=sa.TEXT(),
                    nullable=True)
    op.alter_column('failback', 'state',
                    existing_type=sa.Enum('INCOMPLETE', 'IDLE', 'READY',
                                          'RUNNING', 'SYNCHRONIZED'),
                    nullable=False)
    # ### end Alembic commands ###
