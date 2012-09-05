#!/usr/bin/env python
# encoding: utf-8
"""
ovation.py

Python API for the Ovation Data Management System. This module uses the JPype package
to provide access to Ovation's Java API via CPython.

Created by Barry Wark on 2012-03-16.
Copyright (c) 2012 Physion Consulting LLC. All rights reserved.
"""
from functools import wraps
import platform
import jpype
import os

_initialized = False

OVATION_API_JAR_PATH = "OVATION_API_JAR_PATH"

def _attach_jvm():
    global _initialized
    if not _initialized:
        initialize()
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()


def jvm(f):
    """Wraps a function for JVM access"""
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        _attach_jvm()
        return f(*args, **kwargs)

    return wrapper

def initialize(extra_jars=None):
    """Initialize the Ovation engine"""

    global _initialized

    if not _initialized:
        classpath = {
            "Darwin" : "/opt/ovation/ovation.jar:/opt/ovation/lib/ovation-ui.jar",
            "Linux" : "/usr/ovation/ovation.jar:/usr/ovation/lib/ovation-ui.jar",
            "Windows" : "C:\Program Files\Physion\Ovation\ovation.jar;C:\Program Files\Physion\Ovation\lib\ovation-ui.jar;"
        }

        libpath = {
            "Darwin" : "/opt/ovation/lib:/opt/object/mac86_64/lib",
            "Linux" : "/usr/ovation/lib:/usr/object/linux86_64/lib/",
            "Windows" : "", #Handled by PATH (I think)
        }

        os_name = platform.system()

        if OVATION_API_JAR_PATH in os.environ:
            platformClasspath = os.environ[OVATION_API_JAR_PATH]
        else:
            platformClasspath = classpath[os_name]

        if extra_jars is not None:
            platformClasspath = platformClasspath + os.path.pathsep + os.path.pathsep.join(extra_jars)

        jpype.startJVM(jpype.getDefaultJVMPath(), 'ea',
                        '-Djava.class.path={0} '.format(platformClasspath),
                        '-Djava.library.path={0}'.format(libpath[os_name])
                       )

        _initialized = True

        ovation = ovation_package()
        ovation.Ovation.enableLogging()


def ovation_package():
    return jpype.JPackage('ovation')

@jvm
def version():
    """The Ovation installation version"""
    
    ovation = ovation_package()
    return ovation.Ovation.getVersion()



@jvm
def dataStoreCoordinatorWithConnection(connection):
    """Creates a new DataStoreCoordinator with the given connection string"""
    
    ovation = ovation_package()
    return ovation.DataStoreCoordinator.coordinatorWithConnectionFile(connection)


@jvm
def datetime(*args):
    """Creates a new DateTime object"""
    return _jodatime().DateTime(*args)


@jvm
def timezone_with_id(tzID):
    """Returns the DateTimeZone for the given timezone ID"""
    return _jodatime().DateTimeZone.forID(tzID)


@jvm
def timezone_with_offset(offset_hrs):
    """Returns the DateTimeZone with the given offset (in hours) from UTC"""
    return _jodatime().DateTimeZone.forOffsetHours(offset_hrs)


def _joda():
    return jpype.JPackage("org.joda")

def _jodatime():
    return jpype.JPackage("org.joda.time")

def java_package(package):
    return jpype.JPackage(package)

def java_class(className):
    return jpype.JClass(className)
