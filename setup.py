import setuptools
from os import path

with open('./README.md', 'r') as f:
    long_description = f.read()

with open('./requirements.txt', 'r') as f:
    requirements = [a.strip() for a in f]

setuptools.setup(
    name="rcute-ai",
    version="0.9",
    author="Huang Yan",
    author_email="hyansuper@foxmail.com",
    description="Simple wrapper over some python libs for image/audio detection/recognition etc",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyansuper/rcute-ai",
    packages=['rcute_ai'],
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)