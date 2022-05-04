"""The setup file for pyobjserializer library and pyobjconverter.py utility."""

from setuptools import setup

setup(
    name="pyobjserializer",
    version="1.7",
    description="A library to serialize Python objects and a console tool to convert object from one "
                "format to another",
    author="aneroid11",
    packages=["pyobjserializer"],
    install_requires=["tomli_w", "tomli", "pyyaml"],
    scripts=["pyobjconverter.py"],
)
