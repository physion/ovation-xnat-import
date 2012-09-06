'''
Copyright (c) 2012 Physion Consulting, LLC
'''
__author__ = 'barry'

from ovation.api import datetime
from ovation.xnat.util import iterate_entity_collection, xnat_api_pause


class XnatImportError(StandardError):
    pass

def import_projects(dsc, xnat):
    """
    Import all projects from the given XNAT REST API Interface
    """

    _init_xnat(xnat)

    for project in xnat.select.projects():
        import_project(dsc, project)

    print("Total projects: " + str(len(dsc.getContext().getProjects())))


def import_project(dsc, xnatProject):
    """
    Import a single XNAT project.

    """

    ctx = dsc.getContext()

    xnat_api_pause()
    name = xnatProject.attrs.get('xnat:projectData/name')
    xnat_api_pause()
    purpose = xnatProject.attrs.get('xnat:projectData/description')
    project = ctx.insertProject(name,
        purpose,
        datetime())

    project.addProperty('xnat:datatype', xnatProject.datatype())

    for s in iterate_entity_collection(xnatProject.subjects):
        insert_source(dsc, s)

    xnat_api_pause()
    for k in xnatProject.attrs.get('xnat:projectData/keywords').split():
        project.addTag(k)

    return project

def insert_source(dsc, xnatSubject):
    """
    Insert a single XNAT subject
    """

    sourceID = None
    try:
        sourceID = xnatSubject.id()
    except:
        XnatImportError("Unable to retrieve subject accession ID from " + xnatSubject._uri)

    assert sourceID is not None

    ctx = dsc.getContext()

    src = ctx.sourceForInsertion([sourceID], ['xnat:subjectURI'], [xnatSubject._uri])

    return src


def _init_xnat(xnat):
    xnat.cache.clear()
    xnat.manage.schemas.add('xnat.xsd')
    xnat.manage.schemas.add('fs.xsd')

