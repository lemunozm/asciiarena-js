package com.asciiarena.lib.client.gui.terminal;
import java.awt.event.KeyEvent;

public enum Key
{
    A(KeyEvent.VK_A),
    B(KeyEvent.VK_B),
    C(KeyEvent.VK_C),
    D(KeyEvent.VK_D),
    E(KeyEvent.VK_E),
    F(KeyEvent.VK_F),
    G(KeyEvent.VK_G),
    H(KeyEvent.VK_H),
    I(KeyEvent.VK_I),
    J(KeyEvent.VK_J),
    K(KeyEvent.VK_K),
    L(KeyEvent.VK_L),
    M(KeyEvent.VK_M),
    N(KeyEvent.VK_N),
    O(KeyEvent.VK_O),
    P(KeyEvent.VK_P),
    Q(KeyEvent.VK_Q),
    R(KeyEvent.VK_R),
    S(KeyEvent.VK_S),
    T(KeyEvent.VK_T),
    U(KeyEvent.VK_U),
    V(KeyEvent.VK_V),
    W(KeyEvent.VK_W),
    X(KeyEvent.VK_X),
    Y(KeyEvent.VK_Y),
    Z(KeyEvent.VK_Z),
    NUM_0(KeyEvent.VK_0),
    NUM_1(KeyEvent.VK_1),
    NUM_2(KeyEvent.VK_2),
    NUM_3(KeyEvent.VK_3),
    NUM_4(KeyEvent.VK_4),
    NUM_5(KeyEvent.VK_5),
    NUM_6(KeyEvent.VK_6),
    NUM_7(KeyEvent.VK_7),
    NUM_8(KeyEvent.VK_8),
    NUM_9(KeyEvent.VK_9),
    RIGHT(KeyEvent.VK_RIGHT),
    DOWN(KeyEvent.VK_DOWN),
    LEFT(KeyEvent.VK_LEFT),
    UP(KeyEvent.VK_UP);
    
    private int keyCode;

    Key(int code)
    {
        this.keyCode = code; 
    }

    public int getCode()
    {
        return keyCode;
    }
}
