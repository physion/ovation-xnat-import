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



DATATYPE_PROPERTY = 'xnat:datatype'

def import_project(dsc, xnatProject):
    """
    Import a single XNAT project.

    """

    xnat_api_pause()
    name = xnatProject.attrs.get('xnat:projectData/name')
    xnat_api_pause()
    purpose = xnatProject.attrs.get('xnat:projectData/description')

    startTime = None
    for s in iterate_entity_collection(xnatProject.subjects):
        src = insert_source(dsc, s)
        sst = src.getOwnerProperty('xnat:INSERT_DATE')
        if sst is not None and (startTime is None or sst.compareTo(startTime) < 0):
            startTime = sst

    for exp in iterate_entity_collection(xnatProject.experiments):
        value = exp.attrs.get(exp.datatype() + '/date')
        print value

    ctx = dsc.getContext()
    project = ctx.insertProject(name,
        purpose,
        startTime if startTime is not None else datetime())

    project.addProperty(DATATYPE_PROPERTY, xnatProject.datatype())


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

    src = ctx.sourceForInsertion([sourceID], ['xnat:subjectURI'], [xnatSubject._uri]).getSource()

    src.addProperty(DATATYPE_PROPERTY, 'xnat:subjectData')

    return src


def _init_xnat(xnat):
    xnat.cache.clear()
    xnat.manage.schemas.add('xnat.xsd')
    xnat.manage.schemas.add('fs.xsd')

