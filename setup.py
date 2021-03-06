import os
import sys
import codecs
from setuptools import setup, find_packages


version = '0.3.0'


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requirements = [
    'django>=1.5',
]


test_requirements = [
    'tox',
    'tox-pyenv',
    'py==1.4.26',
    'pyflakes==0.8.1',
    'pytest==2.6.4',
    'pytest-cache==1.0',
    'pytest-cov==1.8.1',
    'pytest-flakes==0.2',
    'pytest-pep8==1.0.6',
    'pytest-django==2.8.0',
    'cov-core==1.15.0',
    'coverage==3.7.1',
    'execnet==1.3.0',
    'pep8==1.6.2',
    'factory-boy==2.4.1',
    'mock==1.0.1',
    'celery==3.1.16',
    'django-rq==0.7.0',
    'django-redis-cache==1.6.4',
    'hiredis==0.1.6',
]


# sdist
if not 'bdist_wheel' in sys.argv:
    try:
        import importlib
    except ImportError:
        install_requirements.append('importlib>=1.0.3')


# bdist_wheel
extras_require = {
    # http://wheel.readthedocs.org/en/latest/#defining-conditional-dependencies
    ':python_version=="2.6"': ['importlib>=1.0.3'],
    'tests': test_requirements,
    'rq': ['django-rq'],
    'celery': ['celery'],
}


setup(
    name='django-livewatch',
    version=version,
    description=(
        'django-livewatch integrates livewatch.de for django projects'),
    long_description=read('README.rst'),
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    url='https://github.com/moccu/django-livewatch/',
    packages=find_packages(exclude=[
        'livewatch.tests',
    ]),
    install_requires=install_requirements,
    extras_require=extras_require,
    include_package_data=True,
    license='BSD',
    keywords=['livewatch', 'django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    zip_safe=False,
)
