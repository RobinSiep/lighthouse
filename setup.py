from setuptools import setup

requires = [
    'aiohttp',
    'alembic',
    'psycopg2',
    'python-socketio',
    'sqlalchemy',
    'zope.sqlalchemy'
]

setup(
    name='lighthousemaster',
    version='0.1',
    author='Robin Siep',
    author_email='hello@robinsiep.dev',
    install_requires=requires
)
