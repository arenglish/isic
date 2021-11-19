from skimage.color import rgb2gray
from skimage.morphology import (erosion, dilation, opening, closing,  # noqa
                                white_tophat, disk)

def removeHair(image, seSize = 5):
    imClosed = image.copy();
    R = rgb2gray (imClosed[:,:,0])
    G = rgb2gray (imClosed[:,:,1])
    B = rgb2gray (imClosed[:,:,2])
    footprint = disk(seSize)

    Rc = closing(R, footprint)
    Gc = closing(G, footprint)
    Bc = closing(B, footprint)


    imClosed[:,:,0] = Rc
    imClosed[:,:,1] = Gc
    imClosed[:,:,2] = Bc

    return imClosed
