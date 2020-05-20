import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID


"""port

Revision ID: 0852aaf9d3bc
Revises: 128aa8529f40
Create Date: 2020-05-20 08:38:27.936693

"""

# revision identifiers, used by Alembic.
revision = '0852aaf9d3bc'
down_revision = '128aa8529f40'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'port',
        sa.Column('number', sa.Integer(), primary_key=True),
        sa.Column('machine_id', UUID(as_uuid=True), primary_key=True,
                  nullable=False),
        sa.Column('forwarded', sa.Boolean(), default=False, nullable=False),
        sa.ForeignKeyConstraint(['machine_id'], ['machine.id'], )
    )


def downgrade():
    op.drop_table('port')
