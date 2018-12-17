package com.asciiarena.lib.client.gui.terminal;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontFormatException;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;

import javax.swing.JPanel;

public class TerminalPanel extends JPanel implements KeyListener
{
    private static final long serialVersionUID = 6037743281369569724L;

    private static final Color EMPTY_FOREGROUND = Color.WHITE;
    private static final Color EMPTY_BACKGROUND = Color.BLACK;

    private HashSet<Integer> keysDown;
    private ArrayList<Integer> keysUp;
    private Tile[][] tiles;
    private int tileHeight;
    private int tileWidth;
    private Font font;

    public static Font loadFont(String fontPath)
    {
        try
        {
            InputStream is = TerminalPanel.class.getResourceAsStream(fontPath);
            if(is != null)
            {
                return Font.createFont(Font.TRUETYPE_FONT, is);
            }
            return new Font("Courier", Font.BOLD, 1); 
        } 
        catch (FontFormatException | IOException e)
        {
            e.printStackTrace();
            return null;
        }
    }

    public TerminalPanel(int rows, int columns, int fontHeight, Font font)
    {
        this.keysDown = new HashSet<Integer>();
        this.keysUp = new ArrayList<Integer>();
        this.tiles = new Tile[rows][columns];
        this.tileWidth = fontHeight / 2;
        this.tileHeight = fontHeight;

        Font baseFont = (font == null) ? loadFont("/resources/fonts/FuraMono-Medium Powerline.otf") : font;
        FontMetrics metrics = getFontMetrics(baseFont.deriveFont((float) fontHeight));
        this.font = baseFont.deriveFont(fontHeight * ((float) fontHeight / 2) / metrics.stringWidth("A"));

        for(int x = 0; x < tiles.length; x++)
        { 
            for(int y = 0; y < tiles[0].length; y++)
            {
                tiles[x][y] = new Tile(Tile.NONE, EMPTY_FOREGROUND, EMPTY_BACKGROUND);
            }
        }

        setPreferredSize(new Dimension(rows * fontHeight / 2, columns * fontHeight));
        setDoubleBuffered(true);
        addKeyListener(this);
    }

    public void paint()
    {
        Graphics2D g2 = (Graphics2D) getGraphics();
        g2.setRenderingHint(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
		g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
		g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g2.setFont(font);

        FontMetrics metrics = getFontMetrics(font);
        int offsetY = metrics.getLeading() + metrics.getAscent() + metrics.getDescent(); //Works fine but check this
        offsetY -= (tileHeight - metrics.getHeight());

        for(int x = 0; x < tiles.length; x++)
        { 
            for(int y = 0; y < tiles[0].length; y++)
            {
                Tile tile = tiles[x][y];
                g2.setColor(tile.getBackground());
                g2.fillRect(x * tileWidth, y * tileHeight, tileWidth, tileHeight);
                if(font.canDisplay(tile.getCharacter()))
                {
                    g2.setColor(tile.getForeground());
                    int charX = x * tileWidth;
                    int charY = offsetY + y * tileHeight;
                    g2.drawString(String.valueOf(tile.getCharacter()), charX, charY);
                }
            }
        }
    }

    public void collapseKeysBuffer()
    {
        for(int keyUp: keysUp) 
        {
            keysDown.remove(keyUp);
        }
        keysUp.clear();
    }

    @Override
    public void keyPressed(KeyEvent e)
    {
        keysDown.add(e.getKeyCode());
    }

    @Override
    public void keyReleased(KeyEvent e)
    {
        keysUp.add(e.getKeyCode());
    }

    @Override
    public void keyTyped(KeyEvent e)
    {
    }

    public boolean isKeyDown(int keyCode)
    {
        return keysDown.contains(keyCode);
    }

    public Tile[][] getTiles()
    {
        return tiles;
    }
}
