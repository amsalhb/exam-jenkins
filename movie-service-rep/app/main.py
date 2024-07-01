from fastapi import FastAPI
from app.api.movies import movies
from app.api.db import metadata, database, engine


app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")

def create_database_schema():
    metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    await database.connect()
    create_database_schema()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])
