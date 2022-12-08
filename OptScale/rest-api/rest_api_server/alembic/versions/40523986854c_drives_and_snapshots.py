""""drives_and_snapshots"

Revision ID: 40523986854c
Revises: 5bfe31fe2892
Create Date: 2017-01-13 11:45:31.138380

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import false
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '40523986854c'
down_revision = '5bfe31fe2892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('drive',
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('failover_id', sa.String(length=36), nullable=True),
    sa.Column('fatcow_id', sa.String(length=255), nullable=True),
    sa.Column('conn_str', sa.String(length=255), nullable=True),
    sa.Column('state', sa.Enum('PENDING', 'PREPARATION', 'PARTITIONING', 'P2V', 'READY', 'DELETING', 'ERROR', name='drivestates'), nullable=True),
    sa.Column('error_cause', sa.TEXT(), nullable=True),
    sa.Column('meta', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['failover_id'], ['failover.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('snapshot_drive_association',
    sa.Column('snapshot_id', sa.String(length=36), nullable=True),
    sa.Column('drive_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['drive_id'], ['drive.id'], ),
    sa.ForeignKeyConstraint(['snapshot_id'], ['snapshot.id'], )
    )
    op.drop_column('failover', 'ram')
    op.drop_column('failover', 'cpu')
    op.add_column('snapshot', sa.Column('empty', sa.Boolean(), nullable=True,
                                        server_default=false()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('snapshot', 'empty')
    op.add_column('failover', sa.Column('cpu', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('failover', sa.Column('ram', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('snapshot_drive_association')
    op.drop_table('drive')
    # ### end Alembic commands ###
