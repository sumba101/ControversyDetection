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
	temp,percentage=driverFunction(receive.url)
	# Example values for what should be returned above
	# percentage= None or 90
	# temp = {"Our progress on vaccinations is ...":True,"Gun violence in this country ...":True,"This isn't complicated":False}
	return {"data":temp, "percentage":percentage}
