from setuptools import find_packages, setup

setup(
    name='website-glen',
    version='1.0.0',
    author='Cameron Ridderikhoff',
    author_email="cameronridderikhoff@gmail.com",
    url="https://github.com/UhrigLab/Website_Glen",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
