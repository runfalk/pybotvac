import io
import os

from setuptools import setup


def read_file(path, encoding="utf8", default=None):
    try:
        # Calculate the absolute path relative to this file
        absolute_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            path,
        )

        # Use io.open since it works the same in Python 2 and 3
        with io.open(absolute_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return default


setup(
    name="PyBotVac",
    version="0.1.0",
    description="Unofficial pythonic API for Neato BotVac",
    long_description=read_file("README.rst"),
    license="BSD",
    author="Andreas Runfalk",
    author_email="andreas@runfalk.se",
    url="https://github.com/runfalk/pybotvac/",
    packages=["pybotvac"],
    zip_safe=False,
    platforms="any",
    install_requires=[
        "requests",
        "requests-oauthlib",
    ],
)
