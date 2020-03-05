from setuptools import setup

requires = [
    'aiohttp',
    'aiohttp-security',
    'alembic',
    'marshmallow',
    'psycopg2',
    'pycrypto',
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
