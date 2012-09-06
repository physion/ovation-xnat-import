'''
Copyright (c) 2012 Physion Consulting, LLC
'''
__author__ = 'barry'

from ovation.xnat.util import xnat_api_pause
from nose.tools import eq_, istest

from ovation.api import datetime

from ovation.xnat.test.OvationTestBase import OvationTestBase


class ImportingProjects(OvationTestBase):

#    @istest
#    def should_import_all_projects_form_xnat(self):
#        central = Interface(os.environ["XNAT_URL"],
#            os.environ["XNAT_USER"],
#            os.environ["XNAT_PASSWORD"])
#        import_projects(self.dsc, central)
#
#        ctx = self.dsc.getContext()
#        projects = ctx.getProjects()
#
#        eq_(len(projects), len(central.select.projects().get()))


    @istest
    def should_import_project_name_and_purpose_from_entity_attributes(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.getProjects()[0]

        xnat_api_pause()
        expectedName = xnatProject.attrs.get('xnat:projectData/name')
        xnat_api_pause()
        expectedPurpose = xnatProject.attrs.get('xnat:projectData/description')

        eq_(project.getName(), expectedName)
        eq_(project.getPurpose(), expectedPurpose)

    @istest
    def should_import_project_keywords(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.getProjects()[0]

        xnat_api_pause()
        expectedKeywords = xnatProject.attrs.get('xnat:projectData/keywords').split()
        for k in expectedKeywords:
            assert k in project.getTags()

    @istest
    def should_set_project_datatype_property(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.getProjects()[0]

        eq_(project.getOwnerProperty('xnat:datatype'), 'xnat:projectData')

    @istest
    def should_set_project_start_date_from_earliest_subject_insertion_date(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.getProjects()[0]

        assert project.getStartTime().equals(datetime())





