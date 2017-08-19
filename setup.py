from setuptools import setup

setup(
    name="PyBotVac",
    version="0.1.0",
    description="Unofficial pythonic API for Neato BotVac",
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
