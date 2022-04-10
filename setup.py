import setuptools

from deepfolder import remove

remove("./build")
remove("./dist")
remove("./file_handling.egg-info")

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read()

setuptools.setup(
    name="file-handling",
    version="1.0.1",
    author="sotaneum",
    author_email="gnyontu39@gmail.com",
    description="file_handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sotaneum/file-handling",
    packages=setuptools.find_packages(exclude=['exmple']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires='>=3.6',
)
