from fastapi import FastAPI, HTTPException, APIRouter
import schemas.request as request_schema
from schemas.detail import EventDetail
from functions.livepocket import get_livepocket_data

router = APIRouter()


@router.post("/v1/detail", response_model=EventDetail)
async def get_detail(req: request_schema.Request):
    if req.site == "livepocket":
        try:
            data: EventDetail = get_livepocket_data(req.url)
        except:
            raise HTTPException(status_code=404, detail="Invalid Url")
        else:
            return data
    else:
        raise HTTPException(status_code=404, detail="Invalid Site")

@router.get("/v1/test")
async def test(req: request_schema.Request):
    print(req.url)