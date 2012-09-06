__author__ = 'barry'

from pyxnat.core import Interface
from pyxnat.core.attributes import EAttrs as Attributes

from pprint import  PrettyPrinter

def display_project_structure(url, username=None, password=None):
    if username is None:
        xnat = Interface(url, anonymous=True)
    else:
        xnat = Interface(url, username, password)

    xnat.cache.clear()

    # For central.xnat.org
    xnat.manage.schemas.add('xnat.xsd')
    xnat.manage.schemas.add('fs.xsd')

    for p in xnat.select.projects():
        _display_project(p)



def print_entity_info(entity, info_indent=2):
    pp = PrettyPrinter(indent=info_indent)
    try:
        if len(entity.attrs()) > 0:
            entity_attributes = Attributes(entity)
            for attr in entity.attrs():
                if not ((attr[-1] == 's') or len(attr.split('/')) > 2):
                    try:
                        value = entity_attributes.get(attr)
                        pp.pprint("  " + attr + ": " + value)
                    except StandardError:
                        pp.pprint("  " + attr + ": <unable to retrieve>")

        pp.pprint("datatype: " + entity.datatype() if entity.datatype() is not None else "<None>")
        pp.pprint("uri: " + entity._uri)
    except StandardError,e:
        print(e)



def _display_project(project):
    print("Project: " + project._uri)
    print_entity_info(project, info_indent=2)

    try:
        for s in project.subjects():
            _display_subject(s)
        for exp in project.experiments():
            _display_experiment(exp)
    except:
        pass

def _display_subject(s):
    pp = PrettyPrinter(indent=4)
    pp.pprint("Subject: " + s._uri)
    print_entity_info(s, info_indent=6)

    # pp.pprint(s.attrs())

def _display_experiment(exp):
    pp = PrettyPrinter(indent=4)
    pp.pprint("Experiment: " + exp._uri)
    print_entity_info(exp, info_indent=6)

    for s in exp.scans():
        pps = PrettyPrinter(indent=6)
        pps.pprint("Scan: " + s.id())
        print_entity_info(s, info_indent=8)

        for r in s.resources():
            for f in r.files():
                print("File: " + f._uri)



if __name__ == '__main__':
    display_project_structure('http://central.xnat.org', username='bwark', password='yeujEhT9XLssXuoW2bzv')



