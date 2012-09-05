__author__ = 'barry'

import unittest
import os
import exceptions

from socket import gethostname

import ovation.api as api

from ovation.xnat.test.utils import create_local_database, clean_local_database

# Environment keys for testing
CONNECTION_PATH_KEY = "OVATION_CONNECTION_FILE"
OVATION_FDID_KEY = "OVATION_TEST_FDID"
OVATION_TEST_JAR_PATH_KEY = "OVATION_TEST_JAR_PATH"
TEST_MANAGER_JAR_PATH_KEY = "TEST_MANAGER_JAR_PATH"

class OvationTestException(exceptions.StandardError):
    pass

class OvationTestBase(unittest.TestCase):


    def setUp(self):
        api.initialize(extra_jars=(os.environ[OVATION_TEST_JAR_PATH_KEY], os.environ[TEST_MANAGER_JAR_PATH_KEY]))

        if not CONNECTION_PATH_KEY in os.environ:
            raise OvationTestException("OVATION_CONNECTION_FILE not defined in the test environment")

        self.connection_file_path = os.environ[CONNECTION_PATH_KEY]

        if not os.path.exists(self.connection_file_path):
            create_local_database(self.connection_file_path,
                host=gethostname(),
                federatedDatabaseID=os.environ.get(OVATION_FDID_KEY, None))

        test = api.java_package("us.physion.ovation.test.xnat")
        print(api.java_class("java.lang.System").getProperty("java.class.path"))
        print(api.java_class("java.lang.System").getProperty("java.library.path"))

        tm = api.java_class("us.physion.ovation.test.xnat.OvationTestManager")
        self.test_manager = test.OvationTestManager(self.connection_file_path)
        self.dsc = self.test_manager.setupDatabase()

    def tearDown(self):
        clean_local_database(self.test_manager)



