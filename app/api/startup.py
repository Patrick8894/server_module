from ..common.constants import ENV_FILE
from fastapi import APIRouter
from ..common.logger import startup_logger

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    startup_logger.info("Starting up!")
    startup_logger.info(f"Using ENV File: {ENV_FILE}")