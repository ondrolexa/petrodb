import logging
from contextlib import asynccontextmanager
from os.path import dirname, join

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from petroapi.config import init_db
from petroapi.routers.areas import router as areas_router
from petroapi.routers.profiles import router as profiles_router
from petroapi.routers.profilespots import router as profilespots_router
from petroapi.routers.projects import router as projects_router
from petroapi.routers.samples import router as samples_router
from petroapi.routers.search import router as search_router
from petroapi.routers.spots import router as spots_router
from petroapi.routers.token import router as token_router
from petroapi.routers.users import router as users_router

logger = logging.getLogger("petroapi")

templates = Jinja2Templates(directory=join(dirname(__file__), "templates"))

tags_metadata = [
    {
        "name": "Users",
        "description": "Manage users - only admin",
    },
    {
        "name": "Projects",
        "description": "Manage projects",
    },
    {
        "name": "Samples",
        "description": "Manage samples",
    },
    {
        "name": "Spots",
        "description": "Manage spots",
    },
    {
        "name": "Areas",
        "description": "Manage areas",
    },
    {
        "name": "Profiles",
        "description": "Manage profiles",
    },
    {
        "name": "Profile spots",
        "description": "Manage profile spots",
    },
    {
        "name": "Search",
        "description": "Search interface",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Schema is managed by Alembic migrations (see alembic/), applied via
    # entrypoint.sh before the app starts - not created here.
    init_db()
    yield


app = FastAPI(openapi_tags=tags_metadata, lifespan=lifespan)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning(
        "Integrity error on %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Resource already exists or violates a database constraint"},
    )


app.include_router(token_router)
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(projects_router, prefix="/api", tags=["Projects"])
app.include_router(samples_router, prefix="/api", tags=["Samples"])
app.include_router(spots_router, prefix="/api", tags=["Spots"])
app.include_router(areas_router, prefix="/api", tags=["Areas"])
app.include_router(profiles_router, prefix="/api", tags=["Profiles"])
app.include_router(profilespots_router, prefix="/api", tags=["Profile spots"])
app.include_router(search_router, prefix="/api", tags=["Search"])


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
