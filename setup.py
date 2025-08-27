from setuptools import find_packages, setup

setup(
    name="zhai_db_models",
    version="0.1.0",
    description="Database models for ZeroHungerAI",
    author="R G B",
    author_email="gabrielbongocan@gmail.com",
    packages=["zhai_db_models"],
    install_requires=[
        "geoalchemy2>=0.18.0",
        "sqlalchemy>=2.0.43",
    ],
    python_requires=">=3.11",
    include_package_data=True,
)