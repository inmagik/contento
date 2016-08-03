from setuptools import setup, find_packages
import os
import contento


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Framework :: Django',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
]

INSTALL_REQUIREMENTS = [
    'Django>=1.8',
    'PyYAML>=3.11',
]

setup(
    author='Mauro Bianchi',
    author_email='mauro.bianchi@inmagik.com',
    name='contento',
    version=contento.__version__,
    description='A content management system for Django',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://contento.inmagik.com/',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(exclude=['project', 'project.*']),
    include_package_data=True,
    zip_safe=False,
    #test_suite='runtests.main',
)
