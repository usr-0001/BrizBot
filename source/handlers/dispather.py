from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from aiogram import Dispatcher
import logging
from ftplib import FTP

from source import settings
from source.handlers.PhotoGalery import photo_gallery
from source.handlers import ftp
from source.handlers.VideoGalery import video_gallery

_logger = logging.getLogger(__name__)
__all__ = ["on_startup", "on_shutdown"]

async def on_startup(dispatcher: Dispatcher):
    """
    Handles dispatcher startup event.
    """

    # Get photo pathes
    ftp.cwd(settings.backend.img_gallery_path)
    files = ftp.nlst()
    for file in files:
        if not any(ext in str(file) for ext in ('.PNG', '.png', '.jpg')):
            continue
        photo_gallery.photos.append('briz-berdyansk.com/images/photogallery/' + file)

    imgs = photo_gallery.photos
    imgs.sort()
    for name in imgs:
        print(name)

    # # Get video pathes
    ftp.cwd(settings.backend.video_gallery_path)
    files = ftp.nlst()
    for file in files:
        if not any(ext in str(file) for ext in ('.mp4')):
            continue
        video_gallery.videos.append('briz-berdyansk.com/video/' + file)


async def on_shutdown(dispatcher: Dispatcher):
    """
    Handles dispatcher shutdown event.
    """

    _logger.info("Dispatcher has been shut down")
