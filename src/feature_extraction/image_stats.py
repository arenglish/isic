from skimage.measure import label, regionprops
from skimage.transform import rotate
import math
import numpy
from enum import Enum

class LESION_SIDES(Enum):
    LEFT = 1
    RIGHT = 2

class LesionSide:
    def __init__(self, side: int, image):
        self.side = side
        label_img = label(image)
        regions = regionprops(label_img)
        self.region = regions[0]
        self.image = self.region.image

    # @staticmethod
    # def trimSideImage(cls):
    #     if ()
    # assumes major axis is perfectly horizontal
    @staticmethod
    def flipSide(image):
        flipped = numpy.flip(image, 0)
        return flipped

class OverlapLesionSides:
    def __init__(self, left: LesionSide, right: LesionSide):
        sizeX = max(left.image.shape[1], right.image.shape[1])
        sizeY = max(left.image.shape[0], right.image.shape[0])
        self.image = numpy.ndarray(shape=[sizeY, sizeX], dtype=bool, buffer=numpy.full(shape=[sizeY, sizeX], fill_value=False))
        lIm = numpy.flip(left.image, 1)
        self.flippedLeft = lIm
        self.area = 0

        for y in range(0, len(self.image) - 1):
            for x in range(0, len(self.image[0]) - 1):
                leftSideHasPixel = False
                if ((len(lIm[0]) - 1) >= x and (len(lIm) - 1) >= y):
                    leftSideHasPixel = lIm[y, x] == True
                rightSideHasPixel = False
                if ((len(right.image[0]) - 1) >= x and (len(right.image) - 1) >= y):
                    rightSideHasPixel = right.image[y, x] == True

                if leftSideHasPixel and rightSideHasPixel:
                    self.image.itemset((y, x), False)
                elif leftSideHasPixel or rightSideHasPixel:
                    self.area = self.area + 1
                    self.image.itemset((y, x), True)


class LesionMaskStats:
    def __init__(self, image):
        self.region = LesionMaskStats.largestRegion(image)
        self.image = rotate(image, -1*self.region.orientation*180/math.pi)
        self.region = LesionMaskStats.largestRegion(self.image)
        self.sides = LesionMaskStats.majorSides(self)
        self.overlapped = OverlapLesionSides(self.sides[1], self.sides[0])

    @staticmethod
    def largestRegion(image):
        im = image.copy()

        label_img = label(im)
        regions = regionprops(label_img)
        largestRegion = False
        i = 0
        for props in regions:
          i = i + 1
          if props.area > (0 if not largestRegion else largestRegion.area):
              largestRegion = props

        return largestRegion

    # assume image has been rotated so major axis is along vertical axis
    @staticmethod
    def majorSides(cls):
        side1Coords = []
        side1LocalCoords = []
        side2Coords = []
        side2LocalCoords = []

        for pixel in cls.region.coords:
            localCoords = [pixel[0] - cls.region.bbox[0], pixel[1] - cls.region.bbox[1]]
            x = pixel[1]
            y = pixel[0]
            if x > cls.region.centroid[1]:
                side1Coords.append(pixel)
                side1LocalCoords.append(localCoords)
            else:
                side2Coords.append(pixel)
                side2LocalCoords.append(localCoords)

        sidesImages = LesionMaskStats.majorSideImages(cls, side1LocalCoords, side2LocalCoords)
        side1 = LesionSide(side=LESION_SIDES.RIGHT, image=sidesImages[0])
        side2 = LesionSide(side=LESION_SIDES.LEFT, image=sidesImages[1])
        return [side1, side2]

    @staticmethod
    def majorSideImages(cls, side1Coords, side2Coords):
        imageX = len(cls.region.image[0])
        imageY = len(cls.region.image)
        side1 = numpy.ndarray(shape=[imageY, imageX], dtype=bool,
                              buffer=numpy.full(shape=[imageY, imageX], fill_value=False))
        side2 = numpy.ndarray(shape=[imageY, imageX], dtype=bool,
                              buffer=numpy.full(shape=[imageY, imageX], fill_value=False))

        for pixel in side1Coords:
            side1.itemset((pixel[0], pixel[1]), True)
        for pixel in side2Coords:
            side2.itemset((pixel[0], pixel[1]), True)

        return [side1, side2]

