import uvicorn
from fastapi import FastAPI, Request
from scraper import driverFunction
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Contro", version="0.0.1", docs_url="/api")

class Receive(BaseModel):
	url: str


@app.post("/")
def index(receive : Receive):
	# return {"data":receive}
	temp=driverFunction(receive.url)
	return {"data":temp}
