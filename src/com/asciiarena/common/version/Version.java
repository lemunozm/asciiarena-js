package com.asciiarena.common.version;

public class Version
{
    public static enum Compatibility {OK, WARNING, ERROR};
    public static final String CURRENT = "1.0.0";

    public static Compatibility check(String version)
    {
        if(version.equals(CURRENT))
        {
            return Compatibility.OK;
        }

        String relevantVersion = version.substring(0, version.lastIndexOf('.'));
        String relevantCurrent = CURRENT.substring(0, version.lastIndexOf('.'));

        if(relevantVersion.equals(relevantCurrent))
        {
            return Compatibility.WARNING;
        }

        return Compatibility.ERROR;
    }
}
