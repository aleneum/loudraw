import sys
from setuptools import setup, find_packages

VERSION = 0.1

tests_require = []
extras_require = {}

extra_setuptools_args = {}
if 'setuptools' in sys.modules:
    extras_require['test'] = ['nose>=0.10.1']
    tests_require.append('nose')
    extra_setuptools_args = dict(
        test_suite='nose.collector',
    )

setup(
    name="transitions",
    version=VERSION,
    description="Draw you soundscape!",
    maintainer='Alexander Neumann',
    maintainer_email='alneuman@techfak.uni-bielefeld.de',
    url='http://github.com/aleneum/loudraw',
    packages=find_packages(exclude=['tests', 'test_*']),
    package_data={'loudraw': ['data/*'],
                  'loudraw.tests': ['data/*']
                  },
    include_package_data=True,
    install_requires=['six'],
    extras_require=extras_require,
    tests_require=tests_require,
    license='MIT',
    download_url='https://github.com/aleneum/loudraw/archive/%s.tar.gz' % VERSION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    **extra_setuptools_args
)