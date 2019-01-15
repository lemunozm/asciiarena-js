## Project modules knowledge:

- Only the `server` and `game_manager`packages have known about connections.
- Ony the `asciiarena.py` package knows about how talk with the user before init the client or server
- `Server` class knows about connections and users, but not about the game.
- `GameManager` class knows about how the game but nothing about the match itself.
- The `Match` package doest know that lives into a server.
