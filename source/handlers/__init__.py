import logging
from ftplib import FTP

from aiogram import Router

from .PhotoGalery import PhotoGallery
from .VideoGalery import VideoGallery
from .command import router as command_handler_router
from .ibutton import router as inline_button_handler_router

__all__ = ["router"]

from .. import settings

_logger = logging.getLogger(__name__)

# Router.
router = Router(name=__name__)
router.include_router(command_handler_router)
router.include_router(inline_button_handler_router)

# Ftp
ftp = FTP()
ret = ftp.connect(host=settings.backend.ftp.host, port=21, timeout=3)
_logger.info(ret)
ret = ftp.login(user=settings.backend.ftp.user, passwd=settings.backend.ftp.passwd)
_logger.info(ret)

# photo_gallery = PhotoGallery()
# video_gallery = VideoGallery()
