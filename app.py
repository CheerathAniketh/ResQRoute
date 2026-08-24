from fastapi import FastAPI
from api.routes import router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="ResQRoute API",
    description="Intelligent Disaster Request Triage & Resource Allocation Engine",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("static/dashboard.html") as f:
        return f.read()

    


app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ResQRoute Gateway Active"}