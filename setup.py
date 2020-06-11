import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="chobo",
        version="0.99.0",
        packages=setuptools.find_packages(),
        description="A Python package for graphical displays",
        long_description="The chobo module is a forked version of the intrographics module developed by Dr. Lisa Torrey.\nIt allows you to create graphical displays in your Python 3 programs. The name chobo (초보) is a Korean word that means a beginner/novice, and the name is to inspire beginners at programming to give it a try.\nIt is written in Python 3, and uses the pygame module as the back-end",
        long_description_content_type="text/markdown",
        url="https://github.com/choongsoo/chobo",
        author="Choong-Soo Lee",
        author_email="clee@stlawu.edu",
        license="GNU",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            "pygame",
            ],
        python_requires='>=3.6',
)


