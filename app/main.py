from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from app.engine.database_engine import (
    create_db_and_tables,
)
from app.routers import (
    data_load_router, file_load_router, backup_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=data_load_router.router)
app.include_router(router=file_load_router.router)
app.include_router(router=backup_router.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app=app)
