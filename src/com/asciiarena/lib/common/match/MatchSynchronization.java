package com.asciiarena.lib.common.match;

import java.util.Date;

public class MatchSynchronization
{
    public static final long FPS = 60;

    private long lastFrameTimestamp;

    public MatchSynchronization() 
    { 
        this.lastFrameTimestamp = 0;
    }

    public void waitForNextFrame()
    {
        long timestamp = new Date().getTime();
        long waitingTime = (1000 / FPS) - (timestamp - lastFrameTimestamp);
        lastFrameTimestamp = timestamp;

        System.out.println("update");
        if(waitingTime > 0)
        {
            try
            {
                Thread.sleep(waitingTime);
            } 
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
        }
    }
}
