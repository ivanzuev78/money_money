import logging
from json import JSONDecodeError
from typing import Any

from aiohttp import web


@web.middleware
async def middleware_logger(request: web.Request, handler: Any) -> web.Response:
    text = f' request {request.method} {request.rel_url}'
    if request.method == 'POST':
        try:
            text += f' body={await request.json()}'
        except JSONDecodeError as e:
            text += f' incorrect body="{await request.content.read()}". Request rejected.'
            logging.debug(text)
            return web.Response(body='Invalid body', headers={'content-type': 'text/plain'}, status=400)
    logging.debug(text)
    response = await handler(request)
    logging.debug(f' response = "{response.text}"')
    return response
