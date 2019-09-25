'''
      configure the library to be installed
'''

from setuptools import setup, find_packages

setup(
    name='lib_connection_sqldb',
    version='1.1.0',
    description='relational database libraries',
    url='',
    author='Erick Henrique',
    author_email='ericles.system@gmail.com',
    license='Public',
    install_requires = [
        'lib_formatter_logger~=1.0',
        'SQLAlchemy~=1.3.0',
        'pymysql~=0.8.0'
    ],
    packages=find_packages(),
    zip_safe=False
)
