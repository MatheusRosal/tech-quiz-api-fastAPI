from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/")
def get_root():
    return {"message": "Minha primeira API"}


@router.get("/health")
def health_check():
    return {"status": "ok", "environment": "docker-dev"}


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")
