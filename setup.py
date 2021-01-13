import os
from setuptools import setup

def get_description(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        contents = fp.read()
    return contents

def get_requirements(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        reqs = fp.readlines()
    return reqs

setup(
    name = "mobistore",
    version = "1.0.0",
    author = "Soumyajit Gorai",
    author_email = "soumya173@gmail.com",
    description = ("A fully responsive and user fiendly online mobile store with attractive admin panel to manage all the stuffs and many more."),
    license = "BSD",
    keywords = "online mobile store app",
    url = "http://packages.python.org/mobistore",
    packages=['mobistore-app', 'tests'],
    install_requires=get_requirements('requirements.txt'),
    long_description=get_description('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
