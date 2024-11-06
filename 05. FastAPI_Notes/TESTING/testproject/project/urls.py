from fastapi import Depends, APIRouter
router = APIRouter()

@router.get(
    "/",
    tags=["Custom Tag"],
    summary="Custom Summary",
    description="Custom Description",
    response_description="Custom Response Description",
)
async def home():
    return 'welcome to here'
