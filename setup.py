import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easytree",
    version="0.1.2",
    author="david.schenck@outlook.com",
    author_email="david.schenck@outlook.com",
    description="A very permissive tree builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschenck/easytree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[]
)
