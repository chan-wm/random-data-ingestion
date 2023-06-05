from setuptools import find_packages, setup

setup(
    name="random-data-ingestion",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        "requests==2.28.2",
        "typed-argument-parser==1.7.2",
        "pymongo==4.3.3",
        "psycopg2==2.9.6"
    ],
    extras_require={
        "testing": [
            "pytest==7.2.0",
            "pytest-mock==3.10.0",
            "requests-mock==1.10.0"
        ]
    },
)
