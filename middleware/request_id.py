import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        # Attach request_id to request state
        request.state.request_id = request_id
        
        response = await call_next(request)
        # Return request_id in headers
        response.headers["X-Request-ID"] = request_id
        
        return response
