from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from discord_interactions import verify_key
from asyncio import iscoroutinefunction as iscoro

from .context import Context


class Server(FastAPI):
    def __init__(self, public_key: str, *args, interactions_path: str = "/interactions", **kwargs):
        super().__init__(*args, **kwargs)

        self.pubkey = public_key
        self.add_route(interactions_path, self.__recv, methods=["POST"])

        self.commands = {}

    async def __recv(self, req: Request):
        body = await req.body()

        sig = req.headers["X-Signature-Ed25519"]
        ts = req.headers["X-Signature-Timestamp"]

        if not verify_key(body, sig, ts, self.pubkey):
            raise HTTPException(400)

        data = await req.json()
        context = Context(data)

        name = context.name
        if name in self.commands:
            result = await self.commands[name](context)
            if isinstance(result, JSONResponse):
                return result

            raise Exception("Command responses must be valid JSONResponse objects.")

        raise HTTPException(404, "Command not found.")

    def add_command(self, func, name: str = None):
        name = name or func.__name__

        if not iscoro(func):
            raise TypeError("Command functions must be coroutines.")

        self.commands[name] = func

    def command(self, name=None):
        def decorator(func):
            self.add_command(func, name)

        return decorator
