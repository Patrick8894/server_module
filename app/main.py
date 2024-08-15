from fastapi import FastAPI

server = FastAPI(root_path="/api")

@server.get("/")
def read_root():
    return {"Hello": "World"}