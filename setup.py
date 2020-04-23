from setuptools import setup

requires = [
    'aiohttp',
    'aiohttp-security',
    'aiohttp_session',
    'alembic',
    'marshmallow',
    'psycopg2',
    'pycrypto',
    'python-socketio',
    'sqlalchemy',
    'zope.sqlalchemy'
]

dev_requires = [
    'aiohttp-devtools'
]

setup(
    name='lighthouse',
    version='0.1',
    author='Robin Siep',
    author_email='hello@robinsiep.dev',
    install_requires=requires,
    extras_require={'dev': dev_requires}
)
