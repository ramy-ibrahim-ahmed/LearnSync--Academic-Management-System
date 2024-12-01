from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import course, user, sections
from .helpers.database import ENGINE, BASE


async def init_db():
    async with ENGINE.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        ENGINE.dispose()


app = FastAPI(
    title="LearnSync🎓",
    summary="Provide a powerful Academic management system.",
    #     description="""
    # **Key Features:**
    # * **Sign up:** User join the system with his data and get an access token.
    # * **Sign in:** Validate authentication and get an access token.
    # * **Delete me:** Exit the system and remove your data.
    # * **Get me:** Get User data.
    # """,
    version="0.0.1",
    contact={
        "name": "Ramy Ibrahim",
        "email": "ramyibrahim987@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(course.router)
app.include_router(sections.router)
