from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/")
def save_image(file: UploadFile):
    """Загрузка изображений"""
    ImagesService().upload_image(file)
