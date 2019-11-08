import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sirtetris',
    version='0.1.6',
    scripts=[],
    author="Sven Cannivy",
    author_email="sven.cannivy@gmail.com",
    description="Tetris bot engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svencan/sirtetris",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )