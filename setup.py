import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easytree",
    version="0.1.8",
    author="david.schenck@outlook.com",
    author_email="david.schenck@outlook.com",
    description="A fluent tree builder, useful to create multi-level, nested JSON configurations.",
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
