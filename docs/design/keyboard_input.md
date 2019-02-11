# Input from the keyboard

## 1º approach: curses input
The curses library do not manage the key events itself, the key pressed events is managed by the terminal and pass the value of the input to *curses*.
The way to pass it is similar to reading from *stdin*.
For that *curses* can not pass information about key released concept, only about "key pressed" concept (a new character written).
Only with the power of *curses* it is not possible to perform a real arcade game because of the lack of keys released."

## 2º approach: key logger events
A key logger is able to read directly from the keyboard events.
This allow to manage both key pressed and key released events.
The problem with the key loggers is that the event comes directly from the OS without knowledge about the application focus.
Also, *curses* do not give you information about if the terminal has the focus or not.
With the key logger approach, any key, can affect to the game, even when it has not the focus.

## 3º approach: curses and key logger mix
This approach focused into getting the key pressed events from *curses* and the key released events from the key logger.
With this method, we only process the real application key events comming from the *curses* and we are able to know when the key is released.

For implementation details, see the [keyboard.py](../../asciiarena/client/keyboard.py) module
