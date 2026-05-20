from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.middleware("http")
async def add_student_id_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Student-ID"] = "23168"
    return response


@app.get("/")
async def home():
    return {"message": "StudySync Backend Running"}