import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shapy-Leoturos", 
    version="0.0.1",
    author="Leo Turowski",
    author_email="leo.turowski@fau.de",
    description="A small package for quick conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karhunenloeve/Shapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)