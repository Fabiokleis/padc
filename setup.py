from setuptools import setup, find_packages


with open("README.md", 'r') as f:
    long_description = f.read()

with open("LICENSE", 'r') as f:
    l = f.read()

setup(
    name="p_ad",
    version="0.1.3",
    description="lab using python-ldap lib to create connection with Active Directory",
    author="Fabio Kleis",
    author_email="fabiohkrc@gmail.com",
    url="https://github.com/Fabiokleis/p_ad",
    license=l,
    long_description=long_description,
    long_description_content_type="text/markdown",
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
        'python-ldap==3.4.3',
        'click==8.1.3',
        'colorama==0.4.6',
        'commonmark==0.9.1',
        'Pygments==2.14.0',
        'rich==12.6.0',
        'shellingham==1.5.0.post1',
        'typer==0.7.0'
    ],
    entry_points={
        'console_scripts': ['padc=cli.__main__:main']
    }
)
