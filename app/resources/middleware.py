import time

from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

async def verify_token(request: Request, call_next):
    routes_without_middleware = ["/docs", "/openapi.json"]
    if request.url.path in routes_without_middleware:
        return await call_next(request)
    # if "token" not in request.headers:
    #     return Response(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         content=json.dumps({
    #             "message": "Invalid Auth Credential !"
    #         })
    #     )
    return await call_next(request)