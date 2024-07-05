from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class PhotoGallery:
    def __init__(self):
        self.photos: list[str] = []

    def length(self):
        return len(self.photos)


photo_gallery = PhotoGallery()
