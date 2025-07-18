# GameStuff-client
The client code for my Steam-like game launcher.  
This connects to a private API server (not open source), but the client itself is fully open source and free to use.


## Table of Contents

- [How to Run](#how-to-run)
- [Dependencies](#dependencies)
- [API Endpoint Map](#api-endpoint-map)
  - [Auth](#auth)
    - [`POST /auth/register`](#post-authregister)
    - [`POST /auth/login`](#post-authlogin)
  - [Games](#games)
    - [`GET /games/`](#get-games)
    - [`GET /games/{game_id}`](#get-gamesgame_id)
  - [Marketplace](#marketplace)
    - [`GET /marketplace/`](#get-marketplace)
    - [`POST /marketplace/`](#post-marketplace)
  - [Library](#library)
    - [`GET /library/{user_id}`](#get-libraryuser_id)
    - [`POST /library/`](#post-library)
- [Notes](#notes)


## How to run
You can either:

- Download the `.exe` from **Releases** (cleaner folder)
- Or download the source and run:

```bash
python main.py
```

> Note:
> I am using Python version 3.12.7, but you can test what version it works with because I don't know what else works with it tbh.

## Dependencies
Probably should put this above but here you go:
```
PyQt5
requests
qasync
aiohttp
```

## API Endpoint Map

These are the main API endpoints the client interacts with — useful for anyone curious.

>Quick note:
>If the API is slow, it’s probably just the server starting up.
>
>Not in my control right now — I’m broke and my router keeps disconnecting my main PC so I can't self host.

---

### Auth

#### POST /auth/register
- Register a new user.

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
- Success:  
  ```json
  { "msg": "User registered successfully" }
  ```
- Failure (username exists):  
  ```json
  { "detail": "Username already exists" }
  ```

---

#### POST /auth/login
- Log in with your credentials.

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
- Success:  
  ```json
  { "msg": "Login successful" }
  ```
- Failure (invalid credentials):  
  ```json
  { "detail": "Invalid credentials" }
  ```

**Usage Notes:**
- authentication is stateless; you must include your username and password in the body of each request that requires authentication.
- Store your username and password securely on the client if you need to re-authenticate.

---

### Games

#### GET /games/
- Get a list of all available games.

**Response:**
```json
[
  {
    "price": 0,
    "description": "Just a game...",
    "title": "game",
    "id": 1,
    "download_url": null,
    "metadata_path": "server_storage/games/game/metadata.json"
  }
]
```

#### GET /games/{game_id}
- Get details for a specific game.

**Response:**
```json
{
  "id": 0,
  "title": "game name",
  "version": "1.0.0",
  "description": "Just a game...",
  "developer": "Dev Name",
  "release_date": "1",
  "icon": "icon.png",
  "screenshot": "screenshot1.png",
  "requirements": {
    "os": "Windows 69",
    "ram": "1 GB",
    "storage": "420 MB",
    "cpu": "Sigma Core",
    "gpu": "Integrated"
  }
}
```

---

### Marketplace

#### GET /marketplace/games
- List all items available in the marketplace.

**Response:**
```json
[
  {
    "id": "game",
    "title": "game",
    "version": "1.0.0",
    "description": "Just a game...",
    "developer": "Warrick",
    "release_date": "1",
    "icon": "icon.png",
    "screenshot": "screenshot1.png",
    "requirements": {
      "os": "Windows 69",
      "ram": "420 GB",
      "storage": "150 MB",
      "cpu": "Sigma Core",
      "gpu": "Any"
    }
  }
]
```

---

### Library

#### GET /library/{user_name}
- Get the list of games owned by a user.

**Response:**
```json
{
  "library": [
    "game"
  ]
}
```

#### POST /library/add
- Add a game to the user's library.

**Request Body:**
```json
{
  "username": "username",
  "password": "password"
  "game_name": "game name"
}
```

**Response:**
```json
{ "msg": "Game added to library" }
```

---

> ## Notes
>
> All endpoints that modify data (such as adding to the library, and in the future, to the marketplace) require authentication.
>
> If anything is wrong in the API documentation, feel free to make a issue stating the inaccurate part, and also provide something more accurate if you feel nice :D
>
> Since there's no token system,  include your username/password with each request - just like `/auth/login`.
>
> There is currently no rate limiting, but don’t abuse the API :)
---
