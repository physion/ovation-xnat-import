'''
Copyright (c) 2012 Physion Consulting, LLC. All rights reserved.
'''

from ovation.xnat.importer import DATATYPE_PROPERTY
from ovation.xnat.util import  xnat_api, to_joda_datetime
from nose.tools import istest
from ovation.xnat.test.OvationTestBase import OvationTestBase

class ImportingSessions(OvationTestBase):

    @istest
    def should_import_session_from_subject_as_experiments_with_one_epochgroup(self):
        xnatProject,projectURI = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.objectdWithURI(projectURI)

        for xnatSession in self.xnat.select('/projects/' + xnat_api(xnatProject.id) + '/subjects/*/experiments/*'):
            attrs = xnatSession.attrs
            dtype = xnat_api(xnatSession.datatype)
            datestr = xnat_api(attrs.get, dtype + '/date') + ' ' + xnat_api(attrs.get, dtype + '/time')
            startTime = to_joda_datetime(datestr, 'UTC')
            exps = project.getExperiments(startTime)



    @istest
    def should_set_session_datatpe(self):
        self.fail("implement " + DATATYPE_PROPERTY)

    @istest
    def should_import_epochgroup_per_scan(self):
        self.fail("implement")

    @istest
    def should_import_epoch_per_file(self):
        """
        Should import files as URLResponses, not as Resources
        """

        self.fail("implement")
