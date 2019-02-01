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

### 3.1º approach: avoiding the temporal problem
The 3º approach seems to works well but has a temporal problem:
The key released events can be process before the curses gives us the key pressed event.
For example:

The user press key 'A'. The user maintain the key 'A' presed during 5 seconds.
During this time, more key pressed 'A' events comming from the *curses* because more characters have been "written"
(curses manages the input keys as characters from the stdin, so if you hold down a key, after a while, new events are generated).
After the 5 seconds, the released key event comes and is process.
However, the last key pressed event from *curses* has not processed yet, and when is it processed, no key released event will come later.

This is because the logger generates an interrupt for the key events whereas the curses gives the keys on demand.
For that, it is necessary to combine the *key pressed* information from both, the key logger and the *curses* library,
because the first ones always gives the events in order.
You have two types of information:
* key pressed events ordered respect the key released events but with global information (the key logger).
* key pressed events that not have temporal correlation with the released events but locals to the current application.

From the combination on this two types of key pressed events we can construct a table with the "real" key values of the current application.
For implementation details, see the [keyboard.py](../../asciiarena/client/keyboard.py) module
