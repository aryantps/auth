from fastapi import FastAPI, APIRouter

from app.controller.token_controller import token_router
from app.controller.user_controller import user_router
from app.db.tortoise_config import TORTOISE_CONFIG

from app.resources.middleware import add_process_time_header, verify_token
from app.resources.on_event import register_startup_event, register_shutdown_event
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise


api_router = APIRouter()
api_router.include_router(token_router,tags=["token"])
api_router.include_router(user_router,tags=["user"])

app = FastAPI(
    title="AuthApp",
    version="1.0.0",
    summary="Microservice to handle auth",
    description="Application supposed to manage auth according to SRP",
    contact={"email" : "aryantpratapsingh@gmail.com"},
)
app.include_router(api_router)


app.middleware("http")(add_process_time_header)
app.middleware("http")(verify_token)

# Adds startup and shutdown events.
# register_startup_event(app)
# register_shutdown_event(app)
@app.on_event("startup")
async def startup():
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()
    register_tortoise(app, config=TORTOISE_CONFIG)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

#
# register_tortoise(
#     app,
#     config=TORTOISE_CONFIG,
#     add_exception_handlers=True,
#     generate_schemas=True,
#     )