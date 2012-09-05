package us.physion.ovation.test.xnat;

import ovation.test.*;

import java.rmi.server.ExportException;

/**
 * Created with IntelliJ IDEA.
 * User: barry
 * Date: 9/5/12
 * Time: 3:34 PM
 * To change this template use File | Settings | File Templates.
 */
public class OvationTestManager extends TestManager {

    private String connectionPath;

    public OvationTestManager(String connectionFilePath) {
        connectionPath = connectionFilePath;
    }

    @Override
    public String getLicenseText() {
        return "crS9RjS6wJgmZkJZ1WRbdEtIIwynAVmqFwrooGgsM7ytyR+wCD3xpjJEENey+b0GVVEgib++HAKh94LuvLQXQ2lL2UCUo75xJwVLL3wmd21WbumQqKzZk9p6fkHCVoiSxgon+2RaGA75ckKNmUVTeIBn+QkalKCg9p1P7FbWqH3diXlAOKND2mwjI8V4unq7aaKEUuCgdU9V/BjFBkoytG8FzyBCNn+cBUNTByYy7RxYxH37xECZJ6/hG/vP4QjKpks9cu3yQL9QjXBQIizrzini0eQj62j+QzCSf0oQg8KdIeZHuU+ZSZZ1pUHLYiOiQWaOL9cVPxqMzh5Q/Zvu6Q==";
    }

    @Override
    public String getLicenseInstitution() {
        return "Institution";
    }

    @Override
    public String getLicenseGroup() {
        return "Lab";
    }

    @Override
    public String getConnectionFile() {
        return connectionPath;
    }

    @Override
    public String getFirstUserName() {
        return "TestUser";
    }

    @Override
    public String getFirstUserPassword() {
        return "password";
    }
}
