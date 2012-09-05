__author__ = 'barry'

import ovation.api as api
from socket import gethostname

def create_local_database(connection_path, host=None, federatedDatabaseID=1):
    if host is None:
        host = gethostname()

    ovation = api.ovation_package()
    ovation.database.DatabaseManager.createLocalDatabase(connection_path,
        host,
        int(federatedDatabaseID))

def clean_local_database(test_manager):
    test_manager.tearDownDatabase()
