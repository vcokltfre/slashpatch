from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from discord_interactions import verify_key


class Server(FastAPI):
    def __init__(self, public_key: str, *args, interactions_path: str = "/interactions", **kwargs):
        super().__init__(*args, **kwargs)

        self.pubkey = public_key
        self.add_route(interactions_path, self.__recv, methods=["POST"])

        self.cogs = {}

    async def __recv(self, req: Request):
        body = await req.body()

        sig = req.headers["X-Signature-Ed25519"]
        ts = req.headers["X-Signature-Timestamp"]

        if not verify_key(body, sig, ts, self.pubkey):
            raise HTTPException(400)

        data = await req.json()
        command = data["data"]

        # TODO: process commands

        return JSONResponse({
            "type": 4,
            "data": {
                "content": "Ok."
            }
        })
