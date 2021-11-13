from fastapi import FastAPI

from routes import monster


app = FastAPI(title="D&D SRD API")


@app.get("/ping")
def ping_route():
    return {"alive": True}


app.include_router(monster.router)
