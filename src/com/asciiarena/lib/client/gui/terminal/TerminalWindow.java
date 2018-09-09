package com.asciiarena.lib.client.gui.terminal;

import java.awt.Dimension;
import java.awt.Font;
import java.awt.Toolkit;

import javax.swing.JFrame;

public class TerminalWindow
{
    private static final int DEFAULT_FONT_SIZE = 20;

    private JFrame frame;
    private TerminalPanel terminalPanel;
    
    public TerminalWindow(String title, int rows, int columns)
    {
        this(title, rows, columns, DEFAULT_FONT_SIZE, null);
    }

    public TerminalWindow(String title, int rows, int columns, int fontHeight)
    {
        this(title, rows, columns, fontHeight, null);
    }

    public TerminalWindow(String title, int rows, int columns, int fontHeight, Font font)
    {
        this.terminalPanel = new TerminalPanel(rows, columns, fontHeight, font);
        terminalPanel.setFocusable(true);

        this.frame = new JFrame(title);
        frame.add(terminalPanel);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.pack();

        Dimension dim = Toolkit.getDefaultToolkit().getScreenSize();
        frame.setLocation(dim.width / 2 - frame.getSize().width / 2, dim.height / 2 - frame.getSize().height / 2);
        frame.setVisible(true);
    }

    public void close()
    {
        frame.setVisible(false);
        frame.dispose();
    }

    public boolean isKeyDown(Key key)
    {
        return terminalPanel.isKeyDown(key.getCode());
    }

    public void show()
    {
        terminalPanel.repaint();
    }

    public Brush createBrush()
    {
        return createBrush(0, 0, getRows(), getColumns());
    }

    public Brush createBrush(int x, int y)
    {
        return createBrush(x, y, getRows() - x, getColumns() - y);
    }

    public Brush createBrush(int x, int y, int width, int height)
    {
        if(x + width <= getRows() && y + height <= getColumns())
        {
            return new Brush(terminalPanel.getTiles(), x, y, width, height);
        }
        else
        {
            try
            {
                throw new TerminalException("Create brush out of the terminal window.");
            }
            catch (TerminalException e)
            {
                e.printStackTrace();
                return null;
            }
        }
    }

    public int getRows()
    {
        return terminalPanel.getTiles().length;
    }

    public int getColumns()
    {
        return terminalPanel.getTiles()[0].length;
    }
}
