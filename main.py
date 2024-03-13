import uvicorn
from fastapi import FastAPI

from analisador.routers import analisador_router

app = FastAPI()
app.include_router(analisador_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001)