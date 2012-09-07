'''
Copyright (c) 2012 Physion Consulting, LLC. All rights reserved.
'''

from ovation.xnat.util import xnat_api, entity_keywords, is_atomic_attribute
from nose.tools import  istest, eq_
from ovation.xnat.test.OvationTestBase import OvationTestBase
from ovation.xnat.importer import import_source


class ImportingEntityMetadata(OvationTestBase):

    @istest
    def should_import_keywords(self):
        xnatProject = self._import_first_project()

        ctx = self.dsc.getContext()
        project = ctx.getProjects()[0]

        tags = entity_keywords(xnatProject)
        actualTags = project.getTags()
        for tag in tags:
            self.assertIn(tag, actualTags)

    @istest
    def should_import_resources(self):
        self.fail("implement")

    @istest
    def should_import_attrs(self):
        self._init_xnat_connection()

        (subject,xnatSubject) = self._import_entity()

        attributes = xnat_api(xnatSubject.attrs)
        attrs = xnatSubject.attrs
        for attr in attributes:
            if is_atomic_attribute(xnatSubject, attrs):
                value = xnat_api(attrs.get, attr)
                eq_(subject.getOwnerProperty(attr), value)


    def _import_entity(self):
        '''
        We could make this import any entity that we know has keywords, attributes, and resources
        '''
        xnatEntity = xnat_api(self.xnat.select('/subjects').first)

        source = import_source(self.dsc, xnatEntity)

        return (source, xnatEntity)
