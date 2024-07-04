class PhotoGallery:
    def __init__(self):
        self.photos: list[str] = []

    def length(self):
        return len(self.photos)


photo_gallery = PhotoGallery()
