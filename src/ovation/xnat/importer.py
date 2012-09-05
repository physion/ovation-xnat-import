__author__ = 'barry'

from pyxnat.core import Interface

def display_project_structure(url):
    xnat = Interface(url, anonymous=True)
    xnat.manage.schemas.add('xnat.xsd')
    xnat.manage.schemas.add('fs.xsd')

    for p in xnat.select.projects():
        display_project(p)


def display_project(project):
    print("Project: " + project.label())
    print("  description: " + project.description())




