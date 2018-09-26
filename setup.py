from setuptools import setup

setup(
    name="Snapshotalyzer",
    version="0.1",
    author="Ranga Roy Koduru",
    license="GPL",
    author_email="rangaroykoduru@gmail.com",
    description="Snapshotalyzer is a tool to manage snapshots of AWS EC2 instances",
    packages=['shotty'],
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    '''
)
