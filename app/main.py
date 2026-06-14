from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.modules.document.router import document_router
from app.modules.search.router import search_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(document_router)
app.include_router(search_router)


@app.get("/scalar")
async def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
