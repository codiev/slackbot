import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'websocket-client',
    'requests',
    'click',
]

setup(
    name='slackbot',
    version='1.0',
    description='Slack Bot which watches on certain events and pass them to specified HTTP service.',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='',
    author_email='',
    url='',
    keywords='slack bot http',
    py_modules=['slackbot'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""\
        [console_scripts]
        slackbot = slackbot:main
    """,
)
