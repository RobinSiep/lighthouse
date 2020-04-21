import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

from lighthouse.lib.settings import settings
from lighthouse.models.oauth import OAuthClient


"""oauth

Revision ID: e99daf480fbd
Revises: f2cd496a9df0
Create Date: 2020-03-05 10:50:08.904856

"""

# revision identifiers, used by Alembic.
revision = 'e99daf480fbd'
down_revision = 'f2cd496a9df0'
branch_labels = None
depends_on = None
default_oauth_fields = ('client_id', 'client_secret')


def upgrade():
    op.create_table(
        'oauth_client',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', UUID(as_uuid=True), unique=True,
                  nullable=False),
        sa.Column('client_secret', sa.String(length=64), nullable=False),
        sa.Column('client_type', sa.Enum('confidential', name='client_type'),
                  nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True)
    )

    op.create_table(
        'oauth_access_token',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('client_id', UUID(as_uuid=True), nullable=False),
        sa.Column('access_token', sa.String(length=64), unique=True,
                  nullable=False),
        sa.Column('token_type', sa.Enum('Bearer', name='token_type'),
                  nullable=False),
        sa.Column('expiry_date', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['oauth_client.id'], ),
    )
    insert_default_credentials()


def insert_default_credentials():
    default_oauth_creds = {k: settings[k] for k in default_oauth_fields if k in
                           settings}
    op.bulk_insert(
        OAuthClient.__table__,
        [{
            'id': str(uuid.uuid4()),
            'client_type': 'confidential',
            'name': "lighthouse client",
            'active': True,
            **default_oauth_creds
        }]
    )


def downgrade():
    op.drop_table('oauth_access_token')
    op.drop_table('oauth_client')
