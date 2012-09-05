ovation-xnat-import
===================

XNAT (REST) import for Ovation


Installation and Setup
======================

pip install -r requirements.txt

JPype
-----


Testing
=======

pip install -r development-requirements.txt

mvn package -f src/java/test-manager/pom.xml

OVATION_API_JAR_PATH (optional)
CONNECTION_PATH_KEY = "OVATION_CONNECTION_FILE"
OVATION_FDID = "OVATION_TEST_FDID"
OVATION_TEST_JAR_PATH = "OVATION_TEST_JAR_PATH"
TEST_MANAGER_JAR_PATH = "TEST_MANAGER_JAR_PATH"
