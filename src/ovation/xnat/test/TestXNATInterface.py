from ovation.xnat.test.OvationTestBase import OvationTestBase

__author__ = 'barry'

from pyxnat.core import Interface

class TestXNATInterface(OvationTestBase):

    def test_connects_to_xnat(self):
        central = Interface('http://central.xnat.org', anonymous=True)
        assert central is not None
