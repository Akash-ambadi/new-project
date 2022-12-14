""""filling_empty_resource_service_name"

Revision ID: 3b13e59e69b1
Revises: f89a4b978e4a
Create Date: 2021-11-09 12:40:25.611612

"""
import os
import logging
import sqlalchemy as sa

from alembic import op
from config_client.client import Client as ConfigClient
from pymongo import MongoClient, UpdateOne
from sqlalchemy import select, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '3b13e59e69b1'
down_revision = 'f89a4b978e4a'
branch_labels = None
depends_on = None

LOG = logging.getLogger(__name__)
DEFAULT_ETCD_HOST = 'etcd'
DEFAULT_ETCD_PORT = 80
BULK_SIZE = 2000


def get_config_client():
    etcd_host = os.environ.get('HX_ETCD_HOST', DEFAULT_ETCD_HOST)
    etcd_port = os.environ.get('HX_ETCD_PORT', DEFAULT_ETCD_PORT)
    config_cl = ConfigClient(host=etcd_host, port=int(etcd_port))
    return config_cl


def get_mongo_collections():
    config_cl = get_config_client()
    conn_string = "mongodb://%s:%s@%s:%s" % config_cl.mongo_params()[:-1]
    mongo_cl = MongoClient(conn_string)
    return mongo_cl.restapi.resources, mongo_cl.restapi.expenses


def get_cloud_accounts(session):
    ca_table = table(
        'cloudaccount',
        column('id',  String()),
        column('deleted_at', sa.Integer())
    )
    cloud_accounts = session.execute(
        select([ca_table]).where(ca_table.c.deleted_at == 0))
    return cloud_accounts


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        ca_ids = [x.id for x in get_cloud_accounts(session)]
    finally:
        session.close()

    resources_collection, expenses_collection = get_mongo_collections()
    total_accounts = len(ca_ids)
    cnt = 0
    for ca_id in ca_ids:
        cnt += 1
        LOG.info('processing cloud_account %s (%s / %s)' % (
            ca_id, cnt, total_accounts))
        resources = resources_collection.find(
            {'cloud_account_id': ca_id, 'service_name': None}, [])
        resource_ids = list(map(lambda x: x['_id'], resources))
        for i in range(0, len(resource_ids), BULK_SIZE):
            bulk_resources = resource_ids[i:i + BULK_SIZE]
            expenses = expenses_collection.aggregate([
                {
                    '$match': {
                        'cloud_account_id': ca_id,
                        'resource_id': {'$in': bulk_resources},
                        'service_name': {'$ne': None}
                    }
                },
                {
                    '$group': {
                        '_id': '$resource_id',
                        'service_name': {'$first': '$service_name'}
                    }
                }
            ])
            updates = []
            for e in expenses:
                updates.append(UpdateOne(
                    filter={
                        'cloud_account_id': ca_id,
                        '_id': e['_id']
                    },
                    update={'$set': {'service_name': e['service_name']}}
                ))
            if updates:
                resources_collection.bulk_write(updates)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
