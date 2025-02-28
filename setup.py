'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    '''
    This function reads the requirements.txt file and returns a list of
    requirements to be installed.
    '''
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines frm the file and remove leading/trailing whitespaces
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('Requirements file not found.')

    return requirement_lst