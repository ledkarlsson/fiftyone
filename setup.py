#!/usr/bin/env python
"""
Installs FiftyOne.

| Copyright 2017-2020, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
import os
from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel


class BdistWheelCustom(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        # make just the wheel require these packages, since they aren't needed
        # for a development installation
        self.distribution.install_requires += [
            "fiftyone-brain>=0.2,<0.3",
            "fiftyone-db>=0.3.0,<0.4",
        ]


VERSION = "0.7.1"


def get_version():
    if "RELEASE_VERSION" in os.environ:
        version = os.environ["RELEASE_VERSION"]
        if not version.startswith(VERSION):
            raise ValueError(
                "Release version does not match version: %s and %s"
                % (version, VERSION)
            )
        return version

    return VERSION


EXTRAS_REQUIREMENTS = {"desktop": ["fiftyone-desktop>=0.8.0,<0.9"]}


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="fiftyone",
    version=get_version(),
    description=(
        "FiftyOne: a powerful package for dataset curation, analysis, and "
        "visualization"
    ),
    author="Voxel51, Inc.",
    author_email="info@voxel51.com",
    url="https://github.com/voxel51/fiftyone",
    extras_require=EXTRAS_REQUIREMENTS,
    license="Apache",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages() + ["fiftyone.recipes", "fiftyone.tutorials"],
    package_dir={
        "fiftyone.recipes": "docs/source/recipes",
        "fiftyone.tutorials": "docs/source/tutorials",
    },
    include_package_data=True,
    install_requires=[
        # third-party packages
        "argcomplete",
        "eventlet",
        "future",
        "Jinja2",
        "mongoengine==0.20.0",
        "motor<3,>=2.3",
        "numpy",
        "packaging",
        "Pillow>=6.2",
        "pprintpp",
        "psutil",
        "pymongo<4,>=3.11",
        "retrying",
        "scikit-image",
        "setuptools",
        "tabulate",
        "tornado>=5.1.1,<7",
        "xmltodict",
        "universal-analytics-python3>=1.0.1,<2",
        # internal packages
        "voxel51-eta>=0.3,<0.4",
        # ETA dependency - restricted to a maximum version known to provide
        # wheels here because it tends to publish sdists several hours before
        # wheels. When users install FiftyOne in this window, they will need to
        # compile OpenCV from source, leading to either errors or a
        # time-consuming installation.
        "opencv-python-headless<=4.4.0.46",
    ],
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={"console_scripts": ["fiftyone=fiftyone.core.cli:main"]},
    python_requires=">=3.6",
    cmdclass={"bdist_wheel": BdistWheelCustom},
)
