import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="chobo",
        version="0.99.3",
        packages=setuptools.find_packages(),
        description="A Python package for graphical displays",
        long_description=long_description,
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


