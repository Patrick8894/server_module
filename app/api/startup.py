from ..common.constants import ENV, TEST_ENV
from fastapi import APIRouter
from ..common.logger import startup_logger

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    startup_logger.info("Starting up!")
    startup_logger.info(f"ENV: {ENV}")
    startup_logger.info(f"TEST_ENV: {TEST_ENV}")