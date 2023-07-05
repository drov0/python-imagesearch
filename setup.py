import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-imagesearch",
    version="1.3.0",
    install_requires=['opencv-python', 'numpy', 'python3_xlib', 'pyautogui', 'mss'],
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
