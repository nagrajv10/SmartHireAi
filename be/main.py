import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # to ensure metadata is populated
from app.elasticsearch_client import init_es_indices
from app.api.endpoints import router as api_router

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_es_indices()
    yield

app = FastAPI(title="SmartHire AI ATS", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def home():
    return {"message": "SmartHire AI Backend Running"}
