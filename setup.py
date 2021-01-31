import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'rcute_ai', 'version.py')) as f:
    ns = {}
    exec(f.read(), ns)
    version = ns['__version__']

with open('./README.md', 'r') as f:
    readme = f.read()

if os.environ.get("RCUTE_AI_RTD") == "1":
    requirements_path = './requirements_rtd.txt'
else:
    requirements_path = './requirements.txt'

with open(requirements_path, 'r') as f:
    requirements = [a.strip() for a in f]

setuptools.setup(
    name="rcute-ai",
    version=version,
    author="Huang Yan",
    author_email="hyansuper@foxmail.com",
    description="Simple wrapper over some python libs for image/audio detection/recognition etc",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/r-cute/rcute-ai",
    packages=['rcute_ai'],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)