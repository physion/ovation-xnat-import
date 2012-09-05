__author__ = 'barry'

import unittest
import os
from socket import gethostname

import ovation.api as api
import jpype

from ovation.xnat.test.utils import create_local_database, clean_local_database

# Environment keys for testing
CONNECTION_PATH_KEY = "OVATION_CONNECTION_FILE"
OVATION_FDID = "OVATION_TEST_FDID"
OVATION_TEST_JAR_PATH = "OVATION_TEST_JAR_PATH"
TEST_MANAGER_JAR_PATH = "TEST_MANAGER_JAR_PATH"

class OvationTestException(Exception):
    pass

class OvationTestBase(unittest.TestCase):


    def setUp(self):
        api.initialize(extra_jars=(os.environ[OVATION_TEST_JAR_PATH], os.environ[TEST_MANAGER_JAR_PATH]))

        if not CONNECTION_PATH_KEY in os.environ:
            raise OvationTestException("OVATION_CONNECTION_FILE not defined in the test environment")

        self.connection_file_path = os.environ[CONNECTION_PATH_KEY]

        if not os.path.exists(self.connection_file_path):
            create_local_database(self.connection_file_path,
                host=gethostname(),
                federatedDatabaseID=os.environ.get(OVATION_FDID, None))

        ovation = api.ovation_package()

        test = jpype.JPackage("us.physion.ovation.test")
        self.test_manager = test.xnat.OvationTestManager(self.connection_file_path)
        self.dsc = self.test_manager.setupDatabase()

    def tearDown(self):
        clean_local_database(self.test_manager)



