import cv2 
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from colors import rgb, hex
import pymysql
from scipy.spatial import distance
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import random, os

class DominantColor(object):
     def __init__(self, counts, rgb):
         self.counts = counts
         self.rgb = rgb

class ColorFind(object):
     def __init__(self, rank, distance, rgb):
         self.rank = rank
         self.distance = distance
         self.rgb = rgb
         self.colorInfo = getColorInformation(rgb)

         
class Color(object):
     def __init__(self, colorname, colorcode, colorid, colortype):
         self.colorname = colorname
         self.colorcode = colorcode
         self.colorid = colorid
         self.colortype = colortype

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
    width, height = img.shape[:2]
    contour_margin = int(width * height * 0.0008)
    print("contour_margin" + str(contour_margin))
    cv2.imshow("img_uncropped", img)
    img = img[contour_margin:width-contour_margin, contour_margin:height-contour_margin]
    cv2.imshow("img_cropped", img)
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
    significant = findSignificantContours(img, sobel_8u)

    # Mask
    mask = sobel.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significant, 255)
    # Invert mask
    mask = np.logical_not(mask)

    #Finally remove the background
    img[mask] = 0;

    #cv2.imshow(path.split('/')[-1], img);
    return img

def getDominantColorsFromImage(img, n_colors): 
    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS  

    _, labels, palette = cv2.kmeans(pixels, n_colors+1, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominantcolors = []    
    for i in range(len(counts)):
        if palette[i][0] > 1 and palette[i][1] > 1 and palette[i][2] > 1 :
           # print("dominant color i=" + str(i) + " " +  str(palette[i]))
            dominantcolors.append(DominantColor(counts[i],tuple(palette[i])))
        else:
            #print("ignored color i=" + str(i) + " " +  str(palette[i]))
            palette2 = np.delete(palette, i, 0)
            counts2 = np.delete(counts, i, 0)
    dominantcolors.sort(key=lambda x: x.counts, reverse=True)
    
    indices = np.argsort(counts2)[::-1]   
    freqs = np.cumsum(np.hstack([[0], counts2[indices]/counts2.sum()]))
    rows = np.int_(img.shape[0]*freqs)
    dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette2[indices[i]])

    return dominantcolors, dom_patch

def hex2rgb(rgb):
    return tuple(hex(rgb).rgb)

def rgb2hex(rgb):
    return str(rgb(rgb).hex)

def changeColorSpace(rgb255in):
    rgb1out = tuple([x/255 for x in rgb255in])
    #print("rgb255in" + str(rgb255in) + ", rgb1out " + str(rgb1out))
    return rgb1out

def getPatchFromColor(colorForPatch, img):
    return np.ones(shape=img.shape, dtype=np.uint8)*np.uint8(colorForPatch)


def getClosestColors(dominantColor, n):
    global availableColors
    availableColorsTuples = getDBColorsAsTuples(availableColors)
    empthy_dict = {}
    for color in availableColorsTuples:
        dist = ColorDistance(changeColorSpace(dominantColor),changeColorSpace(color))
        empthy_dict[dist] = [dominantColor,color]
    sortedDict = sorted(empthy_dict.keys())

    colorResult = []
    for i in range(0,n):
        colorDist = sortedDict[i]
        #print("for i : ",str(i),", colorDist : " + str(colorDist))
        colorRGB = empthy_dict[colorDist][1]
        colorResult.append(ColorFind(i+1,colorDist,colorRGB))
        #print(str(i+1) '. closest Color ',colorName, ' (Distance : ' ,str(colorDist),', RGB : ',str(colorRGB) ,')')
       
    return colorResult

def ColorDistance(rgb1,rgb2):
    #print("ColorDistance of " + str(rgb1) + " and " + str(rgb2))
    color1_rgb = sRGBColor(rgb1[0],rgb1[1], rgb1[2] )
    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_rgb = sRGBColor(rgb2[0],rgb2[1], rgb2[2])
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    #print("ColorDistance of " + str(color1_rgb) + " and " + str(color2_lab) + " = " + str(delta_e))
    return delta_e


def getColorInformation(colorfindRgb):
    global availableColors
    for value in availableColors:
        hex = value['color_code']
        rgb = hex2rgb(hex)
        #print("comparing color rgb: " + str(rgb) + " hex " + hex)
        if rgb == colorfindRgb: 
            #print("found color rgb : " + str(rgb) + " (hex : " + hex + ") matching colorfind : " + str(colorfind) + " -> " +value['color_name'] )
            #print("colorname: " + (value['color_name']))
            return Color(value['color_name'], value['color_code'], value['color_id'], value['color_type'])


def getColorsFromDB():
# Connect to Database
    connection = pymysql.connect(host="localhost",    # your host, usually localhost
                        user="WebDBUser",         # your username
                        passwd="qF2J%9a84zU",  # your password
                        db="LegoSorterDB")        # name of the data base
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    #cursor = connection.cursor()
    sql = "SELECT *  FROM `Colors`"
    cursor.execute(sql)
    colors = cursor.fetchall()
    connection.close()
    #print(colors["color_code"])
    return colors


def getDBColorsAsTuples(colors):
    availableColors = []
    for value in colors:
        hex = value['color_code']
        rgb = hex2rgb(hex)
        availableColors.append(rgb)
    return availableColors


availableColors = getColorsFromDB()
nDominantColors = 5
imgpaths = []

dirpath = '/home/robert/LegoSorter/partimages/temp/'
filenames = random.sample(os.listdir(dirpath), 1)
for fname in filenames:
    srcpath = os.path.join(dirpath, fname)
    imgpaths.append(srcpath)

for imgpath in imgpaths:
    contour = segment(imgpath)

    dominantColors, dom_patch = getDominantColorsFromImage(contour, nDominantColors)

    numberOfColorResults = 4

    Rows = nDominantColors + 1
    Cells = (numberOfColorResults +1) 

    Position = range(1,(numberOfColorResults * nDominantColors) + 1)
    fig = plt.figure(1,figsize=(20, 6))
    first = fig.add_subplot(Rows, Cells ,1)
    first.imshow(contour)
    first.set_title('Original')
    first.axis('off')

    second = fig.add_subplot(Rows, Cells ,2)
    second.imshow(dom_patch)
    second.set_title('Dominant colors')
    second.axis('off')
    cposition= 6
    for j in range(nDominantColors) :
        third = fig.add_subplot(Rows, Cells ,cposition)
        third.imshow(getPatchFromColor(dominantColors[j].rgb,contour ))
        third.set_title(str(j+1) +  ". most dominant")
        third.axis('off')
        third.text(2, 30, str(dominantColors[j].rgb), fontsize=10)
        cposition = cposition + 1 
        ClosestColors  = getClosestColors(dominantColors[j].rgb,numberOfColorResults)

        for i in range(numberOfColorResults):
            #print(str(i) + " Name " + ClosestColors[i].name + " Distance " +str(ClosestColors[i].distance) )
            ax = fig.add_subplot(Rows,Cells ,cposition)
            ax.imshow(getPatchFromColor(ClosestColors[i].rgb,contour ))
            ax.set_title(str(j + 1) + "." + str(ClosestColors[i].rank) + ' ' + ClosestColors[i].colorInfo.colorname)
            ax.text(2, 10, "code: " + str(ClosestColors[i].colorInfo.colorcode), fontsize=10)
            ax.text(2, 20, "dist: " + str(ClosestColors[i].distance), fontsize=10)
            ax.text(2, 30, "id: " + str(ClosestColors[i].colorInfo.colorid), fontsize=10)
            ax.set_xlabel(ClosestColors[i].rgb)
            ax.set_ylabel(Position[i])
            ax.axis('off')
            cposition = cposition + 1 

    plt.show(fig)


#cv2.waitKey(0)