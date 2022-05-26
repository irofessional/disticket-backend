from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def healthcheck_handler():
    return {"ok": True}