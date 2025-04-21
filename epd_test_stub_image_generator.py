import logging
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class EPD(object):
    logger.debug("Initializing STUB EPD")
    
    FULL_UPDATE = 0
    PART_UPDATE = 1
    
    def __init__(self):
        self.width = 122
        self.height = 250

    def init(self, update):
        pass

    def Clear(self, color):
        pass

    def display(self, image):
        pass

    def displayPartial(self, image):
        pass

    def getbuffer(self, image):
        image.save("image.png")