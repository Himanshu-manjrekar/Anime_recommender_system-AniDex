from setuptools import find_packages, setup
from typing import List
import os

TEXT_TO_CLEAR = ["/n", "-e ."]

def get_requirements(file_path:str) -> List[str]:
	# This function will retunr the list of requirements
	requirements = []
	with open(file_path) as file_obj:
		requirements = file_obj.readlines()
		requirements = [req.replace(TEXT_TO_CLEAR[0], " ") for req in requirements]

		if TEXT_TO_CLEAR[1] in requirements:
			requirements.remove(TEXT_TO_CLEAR[1])

	return requirements

setup(
	name = "AniDex",
	version="0.0.1",
	author="himanshu Manjrekar",
	author_email = "david46masscar@gmail.com",
	packages = find_packages(),
	install_requires = get_requirements("requirements.txt"),
)
