from setuptools import setup, find_packages

requires = [
    'flask'
]

setup(
    name='diffweb',
    version='0.0',
    description='Diffweb is a python flask application to diff 2 texts',
    author='Ooi Liang Sun',
    author_email='liangsun.ooi@experian.com',
    keywords='blueprint diffweb ',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)