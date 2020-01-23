import sqlalchemy as sa
from alembic import context, op

${imports if imports else ""}

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}

    if context.config.get_main_option("environment") == "develop":
        create_dummy_data()


def create_dummy_data():
    pass


def downgrade():
    if context.config.get_main_option("environment") == "develop":
        remove_dummy_data()

    ${downgrades if downgrades else "pass"}


def remove_dummy_data():
    pass
