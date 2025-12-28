from fastapi import FastAPI
from database import engine
from notes.models import Base
from routers import notes


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

