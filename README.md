# GameStuff-client
The client code for my Steam-like game launcher. 
This client connects to a private API server (not open source), but the client itself is fully open source and free to use.

## How to run
You can download the .exe in Releases for a cleaner folder, or just download the source and run `main.py`.

> Note:
> I am using Python version 3.12.7, but you can test what version it works with because I don't know what else works with it tbh.

## Dependencies
Probably should put this above but here:
```
PyQt5
requests
qasync
aiohttp
```

## API Endpoint Map

These are the main API endpoints the client interacts with — useful for anyone curious.

---

### Auth

#### `POST /auth/register`
Register a new user.

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

#### `POST /auth/login`
Log in with your credentials.

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

#### `GET /games/`
Get a list of all available games.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Game Title",
    "description": "Game description...",
    "price": 9.99
  }
]
```

#### `GET /games/{game_id}`
Get details for a specific game.

**Response:**
```json
{
  "id": 1,
  "title": "Game Title",
  "description": "Game description...",
  "price": 9.99
}
```

---

### Marketplace

#### `GET /marketplace/`
List all items available in the marketplace.

**Response:**
```json
[
  {
    "id": 1,
    "game_id": 1,
    "seller": "username",
    "price": 7.99
  }
]
```

#### `POST /marketplace/`
Add an item to the marketplace.

**Request Body:**
```json
{
  "game_id": 1,
  "price": 7.99
}
```

**Response:**
```json
{ "msg": "Item added to marketplace" }
```

---

### Library

#### `GET /library/{user_id}`
Get the list of games owned by a user.

**Response:**
```json
[
  {
    "game_id": 1,
    "title": "Game Title"
  }
]
```

#### `POST /library/`
Add a game to the user's library.

**Request Body:**
```json
{
  "user_id": 1,
  "game_id": 1
}
```

**Response:**
```json
{ "msg": "Game added to library" }
```

---

> ## Notes
>
> All endpoints that modify data (such as adding to the library) require authentication.
>
> Since the API does not use tokens, include your username and password in the request body as with `/auth/login`.
>
> There is currently no rate limiting, but don’t abuse the API :)
---