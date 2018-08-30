package com.asciiarena.common.communication;

import java.io.Serializable;

public class Message 
{
    public static class Version implements Serializable
    {
        private static final long serialVersionUID = 6487528050142605112L;

        public String version; 

        public Version() {}
        public Version(String version)
        {
            this.version = version;
        }

        public String toString()
        {
            return String.format("%s | %s", "VERSION", version);
        }
    }

    public static class CheckedVersion implements Serializable
    {
        private static final long serialVersionUID = -4190722298194654981L;

        public String version; 
        public boolean validation; 

        public CheckedVersion() {}
        public CheckedVersion(String version, boolean validation)
        {
            this.version = version;
            this.validation = validation;
        }

        public String toString()
        {
            return String.format("%s | %s | %b", "CHECKED_VERSION", version, validation);
        }
    }
}
