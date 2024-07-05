from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class VideoGallery:
    def __init__(self):
        self.videos: list[str] = []

    def length(self):
        return len(self.videos)


video_gallery = VideoGallery()

