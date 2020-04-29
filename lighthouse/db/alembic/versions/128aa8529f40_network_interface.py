import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID


"""network interface

Revision ID: 128aa8529f40
Revises: e99daf480fbd
Create Date: 2020-04-28 13:52:27.626133

"""

# revision identifiers, used by Alembic.
revision = '128aa8529f40'
down_revision = 'e99daf480fbd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'network_interface',
        sa.Column('name', sa.String(64), primary_key=True),
        sa.Column('machine_id', UUID(as_uuid=True), primary_key=True,
                  nullable=False),
        sa.Column('ip_address', sa.String(16), nullable=False),
        sa.Column('netmask', sa.String(16), nullable=False),
        sa.ForeignKeyConstraint(['machine_id'], ['machine.id'], )
    )


def downgrade():
    op.drop_table('network_interface')
