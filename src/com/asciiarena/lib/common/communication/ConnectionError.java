package com.asciiarena.lib.common.communication;

import java.io.IOException;

import com.asciiarena.lib.common.logging.Log;

public class ConnectionError extends IOException
{
    private static final long serialVersionUID = 9122042020654749501L;

    public ConnectionError(Throwable cause, String formattedAddress)
    {
        super(cause);
        Log.warning("Connection lost: %s", formattedAddress);
    }
}
