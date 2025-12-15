from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
import logging

logger = logging.getLogger(__name__)


class RequestResponseMiddleware:
    """
    Middleware to add request/response validation and logging
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        start_time = time.time()

        # Process the request
        response = await self.app(scope, receive, send)

        # Calculate response time
        process_time = time.time() - start_time
        formatted_time = f"{process_time:.4f}"

        # Log the request
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {formatted_time}s")

        return response


async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add process time header to responses
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response