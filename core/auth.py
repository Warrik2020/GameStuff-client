from core.api import post

async def login(username: str, password: str):
    return post("auth/login", {"username": username, "password": password})

def register(username: str, password: str):
    return post("auth/register", {"username": username, "password": password})
