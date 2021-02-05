import random, os
import cv2 
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import matplotlib.pyplot as plt
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colors import rgb, hex, hsv
import pymysql
import colorsys


##############GET COLORS########################################
def downscaleColorValues(rgb255in):
    rgb1out = tuple([x/255 for x in rgb255in])
    #print("rgb255in" + str(rgb255in) + ", rgb1out " + str(rgb1out))
    return rgb1out

def upscaleColorValues2HSV(rgb1in):
    rgb255out = rgb1in[0]*180,rgb1in[1]*255,rgb1in[2]*255 
    #print("rgb1in" + str(rgb1in) + ", rgb255out " + str(rgb255out))
    return rgb255out

def hex2rgb(rgb):
    return tuple(hex(rgb).rgb)

def rgb2hex(rgb):
    return str(rgb(rgb).hex)

def rgb2hsv(rgb):
    rgb1 = downscaleColorValues(rgb)
    return upscaleColorValues2HSV(tuple(colorsys.rgb_to_hsv(rgb1[0], rgb1[1], rgb1[2])))

def rgb2hls(rgb):
    rgb1 = downscaleColorValues(rgb)
    return upscaleColorValues2HSV(tuple(colorsys.rgb_to_hls(rgb1[0], rgb1[1], rgb1[2])))

class LegoColor(object):
     def __init__(self, colorname, colorcode, colorid, colortype):
         self.colorname = colorname
         self.colorid = colorid
         self.colortype = colortype
         self.hex = colorcode
         self.rgb = hex2rgb(colorcode)
         self.hsv = rgb2hsv(self.rgb)
         self.hsl = rgb2hls(self.rgb)

def getColorsFromDB():
# Connect to Database
    connection = pymysql.connect(host="localhost",    # your host, usually localhost
                        user="WebDBUser",         # your username
                        passwd="qF2J%9a84zU",  # your password
                        db="LegoSorterDB")        # name of the data base
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    #cursor = connection.cursor()
    sql = "SELECT *  FROM `Colors` WHERE parts_count > 100"
    cursor.execute(sql)
    colors = cursor.fetchall()
    connection.close()
    #print(colors["color_code"])
    returnColors = []
    for color in colors:
        legocolor = LegoColor(color['color_name'], color['color_code'], color['color_id'], color['color_type'])
        print(legocolor.colorname  + ", hex: " + str(legocolor.hex) + ", rgb "+ str(legocolor.rgb) + ",hsv " + str(legocolor.hsv)+ ",hsl " + str(legocolor.hsl)) 
        returnColors.append(legocolor)

    return returnColors

############## GET COUNTOURS #########################
def getSobel (channel):

    sobelx = cv2.Sobel(channel, cv2.CV_16S, 1, 0, borderType=cv2.BORDER_REPLICATE)
    sobely = cv2.Sobel(channel, cv2.CV_16S, 0, 1, borderType=cv2.BORDER_REPLICATE)
    sobel = np.hypot(sobelx, sobely)
    return sobel;

def findSignificantContours (img, sobel_8u):
    contours, heirarchy = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    tooSmall = sobel_8u.size * 5 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            #cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.LINE_AA, maxLevel=1)
            significant.append([contour, area])

    significant.sort(key=lambda x: x[1])
    return [x[0] for x in significant];

def segment (path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    blurred = cv2.GaussianBlur(img, (5, 5), 0) # Remove noise

    # Edge operator
    sobel = np.max( np.array([ getSobel(blurred[:,:, 0]), getSobel(blurred[:,:, 1]), getSobel(blurred[:,:, 2]) ]), axis=0 )

    # Noise reduction trick, from http://sourceforge.net/p/octave/image/ci/default/tree/inst/edge.m#l182
    mean = np.mean(sobel)

    # Zero any values less than mean. This reduces a lot of noise.
    sobel[sobel <= mean] = 0;
    sobel[sobel > 255] = 255;

    sobel_8u = np.asarray(sobel, np.uint8)

    # Find contours
    significantcontours = findSignificantContours(img, sobel_8u)

    # Mask
    mask = sobel.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significantcontours, 255)
    # Invert mask
    mask = np.logical_not(mask)

    #Finally remove the background
    img[mask] = 0;

    color_img = cv2.imread(path)
    hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    #cv2.imshow(path.split('/')[-1], img);
    means = []
    stddevs = []
    for contour in significantcontours:
        contour_colors = []
        n_points = len(contour)
        for point in contour:
            x, y = point[0]
            xy_hsv = hsv[y, x]
            contour_colors.append(xy_hsv)
        contour_colors = np.array(contour_colors).reshape(1, n_points, 3)
        mean, stddev = cv2.meanStdDev(contour_colors)
        means.append(mean)
        stddevs.append(stddev)

    print('First mean:')
    print(means[0])
    print('First stddev:')
    print(stddevs[0])

    return img



imagecounter = 1
fig = plt.figure(1,figsize=(20, 6))
fig.subplots_adjust(hspace = .4)
def drawImage(image, titel): 
    global imagecounter
    print(str(imagecounter) + ". image for " + titel)
    new_img = fig.add_subplot(Rows, Cells , imagecounter)
    new_img.imshow(image)
    new_img.set_title(titel)
    new_img.axis('off')
    imagecounter += 1

Rows = 1
Cells = 3
def main():
    getColorsFromDB()
    global Rows
    imagepaths = []
    imagepaths.append('/home/robert/LegoSorter/partimages/collection1/run4/929_344_2020-06-22_12_47_36_x586_y160.jpg')
    imagepaths.append('/home/robert/LegoSorter/partimages/collection1/run4/1158_201_2020-06-24_14_12_27_x738_y46.jpg')

    fig = plt.figure(1,figsize=(20, 6))
    Rows = len(imagepaths)



    for imagepath in imagepaths:
        image = cv2.imread(imagepath)
        drawImage(image,'Original')

        maskedimage = segment(imagepath)
        drawImage(maskedimage,'maskedimage')


    plt.show(fig)

main()