import sqlalchemy as sa
from alembic import op


"""machine

Revision ID: f2cd496a9df0
Revises:
Create Date: 2020-01-23 11:59:00.596958

"""

# revision identifiers, used by Alembic.
revision = 'f2cd496a9df0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'machine',
        sa.Column('id', sa.String(length=32), primary_key=True),
        sa.Column('name', sa.String(length=64), unique=True, nullable=False),
        sa.Column('mac_address', sa.String(length=17), unique=True,
                  nullable=False)
    )


def downgrade():
    op.drop_table('machine')
