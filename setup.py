import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easytree",
    version="0.2.4",
    author="David Schenck",
    author_email="david.schenck@outlook.com",
    description="A recursive dot-styled defaultdict to read and write deeply-nested trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://easytree.readthedocs.io/en/latest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
