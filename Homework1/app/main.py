import time

from fastapi import FastAPI, Request
from routers import router

app = FastAPI(
    title="BaseApp",
    description=("BaseApp"),
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware function counting the time needed to handle the request.

    Args:
        request (Request): HTTP request
        call_next: function while can be called while request is handling

    Returns:
        Response with added header "X-Process-Time" with duration of time
        needed to to handle the request.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
