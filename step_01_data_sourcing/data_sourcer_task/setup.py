import os
import os.path # pathlib?


from setuptools import find_packages
from setuptools import setup


def find_requirements():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    requirements = []

    with open('{0}/requirements.txt'.format(dir_path), 'r') as reqs:
        requirements = reqs.readlines()
    return requirements


if __name__ == "__main__":
    setup(
        name="de_sourcing_task",
        version="0.0.2",
        description="The sourcing is tasked to be completed as a separate installable package",
        packages=find_packages(),
        install_requires=find_requirements(),
        include_package_data=True,
        entry_points={'console_scripts': ['de_source_data = package_data_sourcer_task.api_data_sourcer:run_cli']}
    )