""""add_state_for_constraint_limit_hit"

Revision ID: aaa0e98cbc49
Revises: c1a37bc921c9
Create Date: 2021-12-02 12:23:28.496413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql import table, column
from sqlalchemy import select, String, update

# revision identifiers, used by Alembic.
revision = 'aaa0e98cbc49'
down_revision = 'c1a37bc921c9'
branch_labels = None
depends_on = None

limit_hit_states = sa.Enum('RED', 'GREEN')
CHUNK_UPDATE_SIZE = 100


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('constraint_limit_hit', sa.Column(
        'state', limit_hit_states, nullable=False))
    bind = op.get_bind()
    session = Session(bind=bind)
    org_table = table('organization',
                      column('id', sa.String(36)))
    orgs_stmt = select([org_table.c.id])
    org_ids = [org_info['id'] for org_info in
               session.execute(orgs_stmt)]
    constraint_limit_hit_table = table('constraint_limit_hit',
                                       column('id', String(36)),
                                       column('organization_id', String(36)),
                                       column('state', limit_hit_states))
    try:
        for i in range(0, len(org_ids), CHUNK_UPDATE_SIZE):
            org_id_chunk = org_ids[i:i + CHUNK_UPDATE_SIZE]
            update_stmt = update(constraint_limit_hit_table).values(
                state='RED').where(
                constraint_limit_hit_table.c.organization_id.in_(org_id_chunk))
            session.execute(update_stmt)
        session.commit()
    finally:
        session.close()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('constraint_limit_hit', 'state')
    # ### end Alembic commands ###
