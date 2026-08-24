from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="ResQRoute API",
    description="Intelligent Disaster Request Triage & Resource Allocation Engine",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ResQRoute Gateway Active"}