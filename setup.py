from setuptools import setup

requires = [
    'aiohttp',
    'aiohttp_cors',
    'aiohttp-security',
    'aiohttp_session[secure]',
    'alembic',
    'bcrypt',
    'marshmallow',
    'psycopg2',
    'pycrypto',
    'pytest-aiohttp',
    'python-socketio',
    'sqlalchemy',
    'sqlalchemy_utils',
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
    extras_require={'dev': dev_requires},
    entry_points={
        'console_scripts': [
            "lighthouse = lighthouse.app:main"
        ]
    }
)
