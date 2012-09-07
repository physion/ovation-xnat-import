'''
Copyright (c) 2012 Physion Consulting, LLC
'''
__author__ = 'barry'


from time import mktime, strptime
from datetime import datetime
import ovation.api as api
from ovation.xnat.util import  xnat_api_pause, xnat_api


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

def import_project(dsc, xnatProject, timezone='UTC'):
    """
    Import a single XNAT project.

    """

    projectID = xnat_api(xnatProject.id)
    name = xnat_api(xnatProject.attrs.get,'xnat:projectData/name')
    purpose = xnat_api(xnatProject.attrs.get, 'xnat:projectData/description')

    # Find the earliest session date in the project
    xnat = xnatProject._intf
    sessionTypes = xnat.inspect.experiment_types()
    if len(sessionTypes) == 0:
        sessionTypes = ('xnat:mrSessionData', 'xnat:ctSessionData')
        #raise XnatImportError("No session types defined in database")

    minSessionDate = None
    for sessionType in sessionTypes:
        columns = (sessionType + '/DATE', sessionType + '/PROJECT')
        xnat_api_pause()
        query = xnat.select(sessionType, columns=columns).where([(sessionType + '/Project', '=', projectID), 'AND'])
        sessionDates = [ datetime.fromtimestamp(mktime(strptime(time_str['date'], '%Y-%m-%d %H:%M:%S.%f'))) for
                         time_str in
                         query if len(time_str['date']) > 0]
        if len(sessionDates) > 0:
            for sd in sessionDates:
                if minSessionDate is not None:
                    if sd < minSessionDate:
                        minSessionDate = sd
                else:
                    minSessionDate = sd


    if minSessionDate is not None:
        startTime = api.datetime(minSessionDate.year,
            minSessionDate.month,
            minSessionDate.day,
            minSessionDate.hour,
            minSessionDate.minute,
            minSessionDate.second,
            minSessionDate.microsecond * 1e3,
            api.timezone_with_id(timezone)) #TODO timezone
    else:
        startTime = api.datetime()

    ctx = dsc.getContext()
    project = ctx.insertProject(name,
        purpose,
        startTime)

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

