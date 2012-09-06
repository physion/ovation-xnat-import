__author__ = 'barry'

from pyxnat.core import Interface

from pprint import  PrettyPrinter

def display_project_structure(url, username=None, password=None):
    if username is None:
        xnat = Interface(url, anonymous=True)
    else:
        xnat = Interface(url, username, password)
    xnat.manage.schemas.add('xnat.xsd')
    xnat.manage.schemas.add('fs.xsd')

    for p in xnat.select.projects():
        display_project(p)


def print_entity_info(entity, info_indent=4):
    pp = PrettyPrinter(indent=info_indent)
    pp.pprint(info_indent*" " + "label: " + entity.label() if entity.label() is not None else "<None>")
    pp.pprint(info_indent*" " + "datatype: " + entity.datatype() if entity.datatype() is not None else "<None>")
    pp.pprint(info_indent*" " + "uri: " + entity._uri)
    try:
        pp.pprint(info_indent*" " + "owners: " + entity.owners()[0])
    except:
        pass



def display_project(project):
    print("Project: " + project.id())
    print_entity_info(project)
    #pp.pprint(project.attrs())

    #    values = attrs.mget(project.attrs())
    #    pprint(values)
    #    for attr in attr_names:
    #        if attr in project.attrs():
    #            print("  " + attr + ": " + values[attr])

    for s in project.subjects():
        display_subject(s)
    for exp in project.experiments():
        display_experiment(exp)

def display_subject(s):
    pp = PrettyPrinter(indent=4)
    pp.pprint("Subject: " + s.id())
    print_entity_info(s, info_indent=6)

    # pp.pprint(s.attrs())

def display_experiment(exp):
    pp = PrettyPrinter(indent=4)
    pp.pprint("Experiment: " + exp.id())
    print_entity_info(exp, info_indent=6)

    for s in exp.scans():
        pps = PrettyPrinter(indent=6)
        pps.pprint("Scan: " + s.id())
        print_entity_info(s, info_indent=8)

        for r in s.resources():
            for f in r.files():
                print("File: " + f._uri)







