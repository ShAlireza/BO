from fastapi import FastAPI


from routers import service_router

app = FastAPI()

app.include_router(
    service_router,
    prefix='/api/service',
    tags=['Service']
)