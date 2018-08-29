package main.java.common.communication;

import java.io.Serializable;

public class Message 
{
    public static class Version implements Serializable
    {
        private static final long serialVersionUID = 6487528050142605112L;

        public String version; 

        public String toString()
        {
            return version;
        }
    }

    public static class CheckedVersion implements Serializable
    {
        private static final long serialVersionUID = -4190722298194654981L;

        public String version; 
        public boolean validation; 

        public String toString()
        {
            return version;
        }
    }
}
