package com.asciiarena.lib.common.logging;

public enum TermColor
{
    RESET("\u001B[0m"),
    BLACK("\u001B[0;30m"),
    RED_DARK("\u001B[0;31m"),
    GREEN_DARK("\u001B[0;32m"),
    YELLOW_DARK("\u001B[0;33m"),
    BLUE_DARK("\u001B[0;34m"),
    PURPLE_DARK("\u001B[0;35m"),
    CYAN_DARK("\u001B[0;36m"),
    GREY_LIGHT("\u001B[0;37m"),
    GREY_DARK("\u001B[1;30m"),
    RED("\u001B[1;31m"),
    GREEN("\u001B[1;32m"),
    YELLOW("\u001B[1;33m"),
    BLUE("\u001B[1;34m"),
    PURPLE("\u001B[1;35m"),
    CYAN("\u001B[1;36m"),
    WHITE("\u001B[1;37m");

    private String code; 
    
    TermColor(String code)
    {
        this.code = code;
    }

    @Override
    public String toString()
    {
        return code;
    }
}