from skimage.measure import label, regionprops
from skimage.transform import rotate, rescale
import math
import numpy
from enum import Enum

class LESION_SIDES(Enum):
    LEFT = 1
    RIGHT = 2

class LesionSide:
    def __init__(self, side: int, image):
        self.side = side
        self.image = image

class OverlapLesionSides:
    def __init__(self, left: LesionSide, right: LesionSide):
        sizeX = max(left.image.shape[1], right.image.shape[1])
        sizeY = max(left.image.shape[0], right.image.shape[0])
        #print('(OverlapLesionSides): overlap image dimensions: ', sizeX, ', ', sizeY);
        self.image = numpy.ndarray(shape=[sizeY, sizeX], dtype=bool, buffer=numpy.full(shape=[sizeY, sizeX], fill_value=False))
        lIm = numpy.flip(left.image, 1)
        self.flippedLeft = lIm
        self.area = 0

        # calculate area of non-overlapping pixels
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
    def __init__(self, _image):
        image = rescale(_image, 0.1)
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
        rightSideLocalCoords = []
        leftSideLocalCoords = []

        # divide lesion pixels along centroid
        for pixel in cls.region.coords:
            localCoords = [pixel[0] - cls.region.bbox[0], pixel[1] - cls.region.bbox[1]]
            x = pixel[1]
            if x > cls.region.centroid[1]:
                rightSideLocalCoords.append(localCoords)
            else:
                leftSideLocalCoords.append(localCoords)


        sidesImages = LesionMaskStats.majorSideImages(cls, rightSideLocalCoords, leftSideLocalCoords)

        rightSide = LesionSide(side=LESION_SIDES.RIGHT, image=sidesImages[0])
        leftSide = LesionSide(side=LESION_SIDES.LEFT, image=sidesImages[1])
        return [rightSide, leftSide]

    @staticmethod
    def majorSideImages(cls, rightSideCoords, leftSideCoords):
        # set image sizes to full region size to allow for difference in size between sides
        imageX = len(cls.region.image[0])
        imageY = len(cls.region.image)
        rightSideImage = numpy.ndarray(shape=[imageY, imageX], dtype=bool,
                              buffer=numpy.full(shape=[imageY, imageX], fill_value=False))
        leftSideImage = numpy.ndarray(shape=[imageY, imageX], dtype=bool,
                              buffer=numpy.full(shape=[imageY, imageX], fill_value=False))

        # shift left side to right edge and right side to left edge
        rightEdgeOfLeftSide = max(map(lambda x: x[1], leftSideCoords))
        leftEdgeOfRightSide = min(map(lambda x: x[1], rightSideCoords))

        leftSideShift = imageX - 1 - rightEdgeOfLeftSide
        rightSideShift = leftEdgeOfRightSide

        for pixel in rightSideCoords:
            xVal = pixel[1]

            rightSideImage.itemset((pixel[0], xVal - rightSideShift), True)
        for pixel in leftSideCoords:
            xVal = pixel[1]
            leftSideImage.itemset((pixel[0], xVal + leftSideShift), True)

        return [rightSideImage, leftSideImage]

