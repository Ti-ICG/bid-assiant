from fastapi import APIRouter, FastAPI

from bid_assistant import views


def router_v1():
    router = APIRouter()
    router.include_router(views.router)

    return router


def init_routers(app: FastAPI):
    app.include_router(router_v1(), prefix="/api/v1")
