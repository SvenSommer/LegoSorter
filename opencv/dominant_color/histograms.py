# import the necessary packages
from matplotlib import pyplot as plt
import numpy as np
import argparse
import cv2
import random, os


def graysale_hist(image):
    # convert the image to grayscale and create a histogram
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    plt.figure()
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist)
    plt.xlim([0, 256])
   # plt.show()

def flattened_color_hist(image):
    # grab the image channels, initialize the tuple of colors,
    # the figure and the flattened feature vector
    chans = cv2.split(image)
    colors = ("b", "g", "r")
    plt.figure()
    plt.title("'Flattened' Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    features = []
    # loop over the image channels
    for (chan, color) in zip(chans, colors):
        # create a histogram for the current channel and
        # concatenate the resulting histograms for each
        # channel
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)
        # plot the histogram
        plt.plot(hist, color = color)
        plt.xlim([0, 256])
    
    # here we are simply showing the dimensionality of the
    # flattened color histogram 256 bins for each channel
    # x 3 channels = 768 total values -- in practice, we would
    # normally not use 256 bins for each channel, a choice
    # between 32-96 bins are normally used, but this tends
    # to be application dependent
    print ("flattened feature vector size: " + str(np.array(features).flatten().shape) )

def multi_dim_hist(image):
    # grab the image channels, initialize the tuple of colors,
    # the figure and the flattened feature vector
    chans = cv2.split(image)
   
    # let's move on to 2D histograms -- I am reducing the
    # number of bins in the histogram from 256 to 32 so we
    # can better visualize the results
    fig = plt.figure()
    # plot a 2D color histogram for green and blue
    ax = fig.add_subplot(131)
    hist = cv2.calcHist([chans[1], chans[0]], [0, 1], None,
        [32, 32], [0, 256, 0, 256])
    p = ax.imshow(hist, interpolation = "nearest")
    ax.set_title("2D Color Histogram for Green and Blue")
    plt.colorbar(p)
    # plot a 2D color histogram for green and red
    ax = fig.add_subplot(132)
    hist = cv2.calcHist([chans[1], chans[2]], [0, 1], None,
        [32, 32], [0, 256, 0, 256])
    p = ax.imshow(hist, interpolation = "nearest")
    ax.set_title("2D Color Histogram for Green and Red")
    plt.colorbar(p)
    # plot a 2D color histogram for blue and red
    ax = fig.add_subplot(133)
    hist = cv2.calcHist([chans[0], chans[2]], [0, 1], None,
        [32, 32], [0, 256, 0, 256])
    p = ax.imshow(hist, interpolation = "nearest")
    ax.set_title("2D Color Histogram for Blue and Red")
    plt.colorbar(p)
    # finally, let's examine the dimensionality of one of
    # the 2D histograms
    print ("2D histogram shape: %s, with %d values" % (hist.shape, hist.flatten().shape[0]))

# load the image and show it
imgpaths = []
dirpath = '/home/robert/LegoSorter/partimages/collection1/run8/'
filenames = random.sample(os.listdir(dirpath), 1)
for fname in filenames:
    srcpath = os.path.join(dirpath, fname)
    imgpaths.append(srcpath)

#imgpaths.append('/home/robert/LegoSorter/partimages/collection1/run4/929_344_2020-06-22_12_47_36_x586_y160.jpg')
#imgpaths.append('/home/robert/LegoSorter/partimages/collection1/run4/1158_201_2020-06-24_14_12_27_x738_y46.jpg')
for imagepath in imgpaths:
    image = cv2.imread(imagepath)
    cv2.imshow(imagepath, image)
    graysale_hist(image)
    flattened_color_hist(image)
    multi_dim_hist(image)
plt.show()
