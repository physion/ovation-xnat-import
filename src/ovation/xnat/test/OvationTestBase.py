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

        test = api.ovation_package().test

        self.test_manager = test.TestManager(self.connection_file_path,
            'Institution',
            'Lab',
            'crS9RjS6wJgmZkJZ1WRbdEtIIwynAVmqFwrooGgsM7ytyR+wCD3xpjJEENey+b0GVVEgib++HAKh94LuvLQXQ2lL2UCUo75xJwVLL3wmd21WbumQqKzZk9p6fkHCVoiSxgon+2RaGA75ckKNmUVTeIBn+QkalKCg9p1P7FbWqH3diXlAOKND2mwjI8V4unq7aaKEUuCgdU9V/BjFBkoytG8FzyBCNn+cBUNTByYy7RxYxH37xECZJ6/hG/vP4QjKpks9cu3yQL9QjXBQIizrzini0eQj62j+QzCSf0oQg8KdIeZHuU+ZSZZ1pUHLYiOiQWaOL9cVPxqMzh5Q/Zvu6Q==',
            'TestUser',
            'TestPassword')
        
        self.dsc = self.test_manager.setupDatabase()

    def tearDown(self):
        clean_local_database(self.test_manager)



