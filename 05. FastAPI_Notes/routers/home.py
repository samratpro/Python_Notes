from fastapi import Depends, APIRouter
router = APIRouter()


@router.get(
    "/home/",
    tags=["Custom Tag"],
    summary="Custom Summary",
    description="Custom Description",
    response_description="Custom Response Description",
)
async def home():
    return 'none'
