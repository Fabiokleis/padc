from setuptools import setup, find_packages

setup(
    name="p_ad",
    version="0.1",
    description="lab using python-ldap lib to create connection with Active Directory",
    author="Fabio Kleis",
    author_email="fabiohkrc@gmail.com",
    url="https://github.com/Fabiokleis/p_ad",
    package_dir={'': 'src'},
    packages=find_packages(
                where='src',
                exclude=['tests'], 
                include=[
                    'client', 
                    'client.*', 
                    'msad', 
                    'msad.*'
                    'cli', 
                ]
             ),
    install_requires=[
        'future==0.18.3',
        'pyad==0.6.0',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'python-dotenv==0.21.1',
        'python-ldap==3.4.3'
    ],
    entry_points={
        'console_scripts': ['pacd=cli.__main__:main']
    }
)