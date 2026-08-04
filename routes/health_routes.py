from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_root():
    return {"message": "Minha primeira API"}


@router.get("/health")
def health_check():
    return {"status": "ok"}
