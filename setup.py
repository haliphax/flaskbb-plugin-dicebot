'Allows rolling dice in FlaskBB posts for play-by-post RPGs'

from setuptools import setup, find_packages

setup(
    name='flaskbb-plugin-dicebot',
    packages=find_packages('.'),
    version='1.0',
    author='haliphax',
    author_email='haliphax@github.com',
    description='Allows rolling dice for play-by-post games',
    url='https://github.com/haliphax/flaskbb-plugin-dicebot',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    entry_points={'flaskbb_plugins':
                  ['dicebot = dicebot']},
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
