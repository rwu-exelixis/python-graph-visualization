from setuptools import setup, find_packages

setup(
    name='nvl_package',
    version='0.2.26',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'IPython'
    ],
    package_data={
        'nvl_package': ['dist/base.js'],
    }
)
