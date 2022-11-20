import logging
from typing import Any

from aiohttp import web


@web.middleware
async def middleware_logger(request: web.Request, handler: Any) -> web.Response:
    logging.debug(f' request {request.method} = {await request.json()}')
    response = await handler(request)
    logging.debug(f' response = {response.text}')
    return response
