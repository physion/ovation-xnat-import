'''
Copyright (c) 2012 Physion Consulting, LLC. All rights reserved.
'''

from nose.tools import istest
from ovation.xnat.util import _is_atomic_attribute_in_attrs

@istest
def should_reject_attributes_with_parent():
    candidate = 'ns:class/parents/child'
    attrs = ['ns:class/parents/child', 'ns:class/parents', 'ns:class/atomic']

    assert not _is_atomic_attribute_in_attrs(candidate, attrs)


@istest
def should_reject_attirbutes_with_chidlren():
    candidate = 'ns:class/parents'
    attrs = ['ns:class/parents/child', 'ns:class/parents', 'ns:class/atomic']

    assert not _is_atomic_attribute_in_attrs(candidate, attrs)

@istest
def should_accept_atomic_attributes():
    candidate = 'ns:class/atomic'
    attrs = ['ns:class/parents/child', 'ns:class/parents', 'ns:class/atomic']

    assert _is_atomic_attribute_in_attrs(candidate, attrs)

@istest
def should_reject_attributes_not_in_attrs():
    candidate = 'ns:class/nothere'
    attrs = ['ns:class/parents/child', 'ns:class/parents', 'ns:class/atomic']

    assert not _is_atomic_attribute_in_attrs(candidate, attrs)

