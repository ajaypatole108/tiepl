from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tiepl/__init__.py
from tiepl import __version__ as version

setup(
	name="tiepl",
	version=version,
	description="This app is used to make customisation in erpnext",
	author="Ajay Patole",
	author_email="ajaypatole@dhuparbrothers.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
