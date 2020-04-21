from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from lighthouse.db import Base, get_connection_url
from lighthouse.lib.settings import update_settings

target_metadata = Base.metadata
config = context.config
alembic_settings = config.get_section(config.config_ini_section)
update_settings(alembic_settings)

fileConfig(config.config_file_name)


def run_migrations_offline():
    try:
        url = alembic_settings['sqlalchemy.url']
    except KeyError:
        url = get_connection_url(alembic_settings)

    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    settings_for_engine = {}

    try:
        settings_for_engine['sqlalchemy.url'] = alembic_settings[
            'sqlalchemy.url']
    except KeyError:
        settings_for_engine['sqlalchemy.url'] = get_connection_url(
            alembic_settings)

    connectable = engine_from_config(
        settings_for_engine,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
