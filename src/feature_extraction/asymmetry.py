import math
from matplotlib import pyplot as plt

def plotAsymmetry(stats):
    fig, ax1 = plt.subplots()
    image = stats.image
    region = stats.region
    ax1.imshow(image, cmap=plt.cm.gray)

    y0, x0 = region.centroid
    orientation = region.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * region.minor_axis_length
    y1 = y0 - math.sin(orientation) * 0.5 * region.minor_axis_length
    x2 = x0 - math.sin(orientation) * 0.5 * region.minor_axis_length
    y2 = y0 - math.cos(orientation) * 0.5 * region.minor_axis_length

    ax1.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
    ax1.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
    ax1.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = region.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax1.plot(bx, by, '-b', linewidth=2.5)

    ax1.axis((0, len(stats.image[0]), len(stats.image), 0))

    plt.show()

def getAsymmetryScore(stats, doPlot = False):
    if (doPlot):
        fig, axes = plt.subplots(2, 2)
        axes[0, 0].imshow(stats.sides[1].image, cmap=plt.cm.gray)
        axes[0, 0].set_title('Side A')
        axes[0, 0].axis('off')
        axes[0, 1].imshow(stats.sides[0].image, cmap=plt.cm.gray)
        axes[0, 1].set_title('Side B')
        axes[0, 1].axis('off')

        ## Fold Side A down across major axis
        axes[1, 0].imshow(stats.overlapped.flippedLeft, cmap=plt.cm.gray)
        axes[1, 0].set_title('Side A Flipped')
        axes[1, 0].axis('off')

        ## Fold Side A down across major axis
        axes[1, 1].imshow(stats.overlapped.image, cmap=plt.cm.gray)
        axes[1, 1].set_title('Non-overlapping Region')
        axes[1, 1].axis('off')

    #print('Asymmetrical Area: ', stats.overlapped.area)
    #print('Total Area: ', stats.region.area)
    asymmetryScore = stats.overlapped.area / stats.region.area
    return asymmetryScore
