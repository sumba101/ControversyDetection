import uvicorn
from fastapi import FastAPI, Request
from scraper import driverFunction
from fastapi.responses import HTMLResponse


app = FastAPI(title="Contro", version="0.0.1", docs_url="/api")

@app.get("/{url}")
def index(url: str, request: Request):
    temp=driverFunction(url)
    return {"data":temp}