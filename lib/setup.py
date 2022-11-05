import setuptools
import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent)
from extract_library import __version__


setuptools.setup(
    name="extract_library",
    packages=setuptools.find_packages(),
    version=__version__,
    description="A package that automatically unpacks and modifies data in the /DataModel file of a PBIX",
    url="https://github.com/douglassimonsen/redshift_upload",
    author="Matthew Hamilton",
    author_email="mwhamilton6@gmail.com",
    license="MIT",
    classifiers=[],
    include_package_data=True,
    install_requires=[],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)