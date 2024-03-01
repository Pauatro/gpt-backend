from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from shared.settings import Settings
from users.endpoints import endpoints as users
from conversations.endpoints import endpoints as conversations

logging.config.fileConfig("shared/logging/logging.conf", disable_existing_loggers=False)

app = FastAPI()
app_settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(conversations.router)
