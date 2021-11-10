from fastapi import FastAPI


app = FastAPI(title="D&D 5e SRD API")


@app.get("/")
def home_route():
    return {"alive": True}
