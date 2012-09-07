'''
Copyright (c) 2012 Physion Consulting, LLC
'''
__author__ = 'barry'

from ovation.xnat.util import iterate_entity_collection
from nose.tools import eq_, istest
from ovation.xnat.test.OvationTestBase import OvationTestBase

class ImportingSubjects(OvationTestBase):

    def test_can_retrieve_project_subjects(self):
        central = self._init_xnat_connection()
        assert central.select.projects().first().subjects().first().id() is not None



    @istest
    def should_import_all_subjects_for_project(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()

        for s in iterate_entity_collection(xnatProject.subjects):
            subjectID = s.id()
            sources = ctx.getSources(subjectID)

            eq_(1, len(sources))
            eq_(sources[0].getOwnerProperty('xnat:subjectURI'), s._uri)


    @istest
    def should_set_subject_datatype_property(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()

        for s in iterate_entity_collection(xnatProject.subjects):
            subjectID = s.id()
            sources = ctx.getSources(subjectID)

            eq_(1, len(sources))
            eq_('xnat:subjectData', sources[0].getOwnerProperty('xnat:datatype'))
