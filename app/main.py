from fastapi import FastAPI  # imports the FastAPI class from the fastapi module
from app.routers import user # importing user router from app/routers

app = FastAPI() # Creates an instance of the FastAPI application.
app.include_router(user.router) #Including user router

@app.get("/") #  route decorator
async def root(): #async route handler function
    return {"message": "hello world"}
