from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.models import interview, resume, user  # noqa: F401
from app.routers import auth, career, interview as interview_router, learning, resume as resume_router, skills


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    return {"status": "ok", "service": settings.app_name}


app.include_router(auth.router)
app.include_router(resume_router.router)
app.include_router(skills.router)
app.include_router(career.router)
app.include_router(interview_router.router)
app.include_router(learning.router)
