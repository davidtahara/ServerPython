from fastapi import APIRouter

router = APIRouter(prefix="/analisador", tags=[""])

@router.get("/")
def analisador():
    return {"message": ""}