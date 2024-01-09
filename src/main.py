from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from translation.services.exceptions import NotAllowedException
from translation.endpoints.schemas import PostRequestSchema
from translation.endpoints.exceptions import HttpException
from shared.settings import Settings

app = FastAPI()
app_settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return {"data": "data"}

@app.post("/")
async def post(translation_request: PostRequestSchema):
    try:
        return {"data": "posted"}

    except NotAllowedException:
        raise HttpException


# TODO: add logs
# TODO: add tests
