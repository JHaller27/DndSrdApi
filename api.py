from fastapi import FastAPI


app = FastAPI(title="DnD SRD API")


@app.get("/")
def home():
    return {"alive": True}

