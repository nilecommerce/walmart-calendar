from setuptools import setup

setup(
    name='bambi-engine',
    packages=['bambi_engine'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
