import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="python-imagesearch",
    version="1.2.0",
    install_requires=requirements,
    author="Martin Lees",
    author_email="drov.fr@protonmail.com",
    description="A wrapper around openCv to perform image searching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drov0/python-imagesearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
