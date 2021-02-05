import numpy as np 
import cv2
import matplotlib.pyplot as plt
from models.color import Color
from models.dominantcolor import DominantColor
from models.colorbin import Colorbin
import pymysql



def getColorBinsFromDB():
    global connection, cursor
    #cursor = connection.cursor()
    sql = "SELECT *  FROM `Colors` WHERE lower_treshold IS NOT NULL ORDER BY parts_count asc"
    cursor.execute(sql)
    fetchedcolors = cursor.fetchall()
    colorbins = []
    for value in fetchedcolors:
        color = Color(value['color_name'], value['color_code'], value['color_id'], value['color_type'], threshold2tuple(value['lower_treshold']), threshold2tuple(value['upper_treshold']))
        colorbins.append(Colorbin(color))
    
    return colorbins


def getDominantColorsFromImage(img, n_colors): 
    pixels = np.float32(img.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS  

    _, labels, palette = cv2.kmeans(pixels, n_colors+1, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominantcolors = []    
    for i in range(len(counts)):
            dominantcolors.append(DominantColor(counts[i],tuple(palette[i])))
    dominantcolors.sort(key=lambda x: x.counts, reverse=True)

    return dominantcolors

def getmeancolor(img):
    avg_color = np.array(cv2.mean(img)).astype(np.uint8)
    return avg_color

def CountPixelsGetColorbin(img, colorbins):


    
    # grab the image channels, initialize the tuple of colors,
    # the figure and the flattened feature vector
    chans = cv2.split(img)
    colors = ("b", "g", "r")
    #plt.figure()
    #plt.title("'Flattened' Color Histogram")
    #plt.xlabel("Bins")
    #plt.ylabel("# of Pixels")
    # loop over the image channels
    opencvcolorindex = 2
    normalcolorindex = 0
    intensitycount = 0
    for (chan, color) in zip(chans, colors):
        #print("color " + str(color))
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        intensitycount = 0
        for histbin in hist:
            intensitycount += 1
            for colorbin in colorbins:
                #print("color " + str(color) + " intensity " + str(intensitycount) )
                if intensitycount >  int(colorbin.lower_treshold[opencvcolorindex]) and intensitycount < int(colorbin.upper_treshold[opencvcolorindex]):
                    #print("color " + str(color) + " intensity " + str(intensitycount) + ": Bin '" + str(colorbin.color.colorname) + "' (" + colorbin.lower_treshold[opencvcolorindex] + " - " + colorbin.upper_treshold[opencvcolorindex] + ") earning " + str(histbin[0]) + " points")
                    colorbin.count += histbin[0]
    
        #print("color " + str(color)+ ": " + str(hist))
        #plt.plot(hist, color = color)
        #plt.xlim([0, 256])
        opencvcolorindex = opencvcolorindex - 1 # starting with r, following g and b
        normalcolorindex = normalcolorindex + 1

    colorbins.sort(key=lambda x: x.count, reverse=True)
    # Calculate the confidence by looking at the relative distance of the first pretiction to the next one
    confidence = int(((colorbins[0].count -  colorbins[1].count) / colorbins[0].count)*100)
    if debug:
        for colorbin in colorbins:
            print("\r\nBin '" +  str(colorbin.color.colorname) + "' has " + str(colorbin.count))

    #plt.show()
    return colorbins[0] , confidence
    

def threshold2tuple(treshold):
    t = tuple(treshold.replace("[","").replace("]","").split(","))
    return t

def fitsInBinDominant(color, bin):
    if int(color[2]) > int(bin.lower_treshold[0]) and int(color[1]) > int(bin.lower_treshold[1]) and int(color[0]) > int(bin.lower_treshold[2]):
        if int(color[2]) < int(bin.upper_treshold[0]) and int(color[1]) < int(bin.upper_treshold[1]) and int(color[0]) < int(bin.upper_treshold[2]):
            #print("dcolor" + str(color.rgb) + " fits in bin " + str(bin.color.colorname))
            return True
    return False

def fitsInBinAvg(color, bin):
    if int(color[0]) > int(bin.lower_treshold[0]) and int(color[1]) > int(bin.lower_treshold[1]) and int(color[2]) > int(bin.lower_treshold[2]):
        if int(color[0]) < int(bin.upper_treshold[0]) and int(color[1]) < int(bin.upper_treshold[1]) and int(color[2]) < int(bin.upper_treshold[2]):
            #print("avg" + str(color) + " fits in bin " + str(bin.color.colorname))
            return True
    return False

def CropFromCenter(image, margin):
    height, width = image.shape[:2]
    m = margin
    cx = width / 2
    cy = height / 2
    upper_left = (int(cx - m), int(cy - m))
    bottom_right = (int(cx + m), int(cy + m))
    rect_img = image[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    return rect_img

def histogramBackgroundProjection(target,margin):
    hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

    roi = CropFromCenter(target, margin)
    cv2.imshow("roi", roi)
    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

    # calculating object histogram
    roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )

    # normalize histogram and apply backprojection
    cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
    dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

    # Now convolute with circular disc
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    cv2.filter2D(dst,-1,disc,dst)

    # threshold and binary AND
    ret,thresh = cv2.threshold(dst,50,255,0)
    thresh = cv2.merge((thresh,thresh,thresh))
    res = cv2.bitwise_and(target,thresh)

    #res = np.vstack((target,thresh,res))
    return res

def getTresholdsforColorId(colorid):
    global connection, cursor
    sql = "SELECT lower_treshold, upper_treshold FROM LegoSorterDB.Colors WHERE color_id = " + str(colorid)
    cursor.execute(sql)
    color_code = cursor.fetchone()
    print("Tresholds lower " + color_code["lower_treshold"] + " upper " + color_code["upper_treshold"])
    #return  color_code["lower_treshold"], 

def loadimagepathsfromDB(runid, limit):
    global connection, cursor
    sql = """SELECT pi.path, rp.color_id, c.color_name FROM LegoSorterDB.Recognisedparts rp
                LEFT JOIN LegoSorterDB.Recognisedimages ri ON rp.id = ri.part_id
                LEFT JOIN LegoSorterDB.Partimages pi ON ri.image_id = pi.id
                LEFT JOIN LegoSorterDB.Colors c ON rp.color_id = c.color_id
                WHERE rp.color_id > 0
                AND rp.deleted IS NULL 
                AND pi.deleted IS NULL
                AND rp.run_id = """ + str(runid) + """
                AND ri.score > 0 LIMIT """ + str(limit)
    cursor.execute(sql)
    pathsandcolorids = cursor.fetchall()
    return pathsandcolorids    

def saveimage(img):
    img_name = "should_be_" + str(pathsandcolorid["color_name"]).replace(" ","_") + "_id" + str(pathsandcolorid["color_id"]) + ".png"
    cv2.imwrite(img_name, img)
    print("{} written!".format(img_name))
    return False

def compareAvgColorWithBins(avg_color, bins, image):
    global avgfalsep
    for bin in colorbins:
        if fitsInBinAvg(avg_color, bin):      
            if pathsandcolorid["color_id"] == bin.color.colorid:
                print("+   [Correct bin] Avg (" + str(avg_color[:3]) + ") fits in bin '" + str(bin.color.colorname) + "' (" + str(bin.color.colorid)+ ")")
                return True, bin.color.colorid
            else:
                avgfalsep += 1 
                print("--  [False positive] Avg: " + str(avg_color[:3]) + " fits in bin '" + str(bin.color.colorname) + "' (" + str(bin.color.colorid) +")")
    
    print("-   [No Match] for Avg (" + str(avg_color[:3]) + ")" )
    return False, 0

def getPatchFromColor(colorForPatch, img):
    return np.ones(shape=img.shape, dtype=np.uint8)*np.uint8(colorForPatch)

def hex2rgb(rgb):
    return tuple(hex(rgb).rgb)

def clearColorBins(bins):
    for bin in bins:
        bin.count = 0
    return bins

def compareDominantColorsWithBins(dominantcolors, bins, image):
    global dfalsep
    for dcolor in dominantcolors:
    # print("dcolor: " + format(dcolor.rgb) + ", counts: " + str(dcolor.counts))
        for bin in colorbins:
            if fitsInBinDominant(dcolor.rgb, bin):      
                if pathsandcolorid["color_id"] == bin.color.colorid:
                    print("+   [Correct bin]  Dominamt (" + format(dcolor.rgb) + ") fits in bin '" + str(bin.color.colorname) + "' (" + str(bin.color.colorid) + ")")
                    return True
                else:
                    dfalsep += 1
                    print("--  [False positive] Dominant color: " + format(dcolor.rgb) + ", counts: " + str(dcolor.counts) + " fits in bin '" + str(bin.color.colorname) + "' (" + str(bin.color.colorid) +")" )

    print("-   [No Match] No Dominamt colorMatch (" + format(dcolor.rgb)  + ") ")
        #saveimage(image)         
    return False
# Connect to Database
connection = pymysql.connect(host="localhost",    # your host, usually localhost
                        user="WebDBUser",         # your username
                        passwd="qF2J%9a84zU",  # your password
                        db="LegoSorterDB")        # name of the data base
cursor = connection.cursor(pymysql.cursors.DictCursor)

colorbins = getColorBinsFromDB()

pathsandcolorids = loadimagepathsfromDB(9,200) 

debug = False
dsuccess = 0
dfailure = 0
dfalsep = 0
avgsuccess = 0
avgfailure = 0
avgfalsep = 0
pixelsuccess = 0
pixelnoresult = 0
pixelfalsep = 0
combinedsuccess = 0
combinedfalsep = 0
copmbinedfailure = 0
total = 0
dominantsearch = True
avgsearch = True
pixelcountsearch = True
combinesearch = True
avgcolorid = 0
for pathsandcolorid in pathsandcolorids:

    total += 1
    original = cv2.imread(pathsandcolorid["path"])
    img = histogramBackgroundProjection(original,20)
    print("\r\nTARGET: '" + str(pathsandcolorid["color_name"]) + "' (" + str(pathsandcolorid["color_id"])+ ")")
    #getTresholdsforColorId(pathsandcolorid["color_id"])
    cv2.imshow("img",img)
    if dominantsearch:
        print("Dominant Color Search")
        dominantColors = getDominantColorsFromImage(img, 1)
        if not compareDominantColorsWithBins(dominantColors,colorbins, original):    
            if debug:
                f = plt.figure()
                f.add_subplot(1,2, 1)
                plt.imshow(original[:,:,::-1])
                f.add_subplot(1,2, 2)
                plt.imshow(img[:,:,::-1])
                plt.show()  
            dfailure += 1
        else:
            dsuccess += 1   

    if avgsearch or combinesearch:
        print("AVG Color Search")
        avg_color = getmeancolor(img)
        res, avgcolorid = compareAvgColorWithBins(avg_color,colorbins, original)
        if not res:    
            if debug:
                f = plt.figure()
                f.add_subplot(1,3, 1)
                plt.imshow(original[:,:,::-1])
                f.add_subplot(1,2, 2)
                plt.imshow(img[:,:,::-1])
                f.add_subplot(1,3, 3)
                plt.imshow(getPatchFromColor(avg_color[:3], img)[:,:,::-1])
                #plt.show()  
            avgfailure += 1   
        else: 
            avgsuccess+= 1 

    confidencetrshold = 0
    if pixelcountsearch or combinesearch:
        print("Pixel Counting Search")
        colorbins = clearColorBins(colorbins)
        bestcolorbin, confidence = CountPixelsGetColorbin(img, colorbins)
        if pathsandcolorid["color_id"] == bestcolorbin.color.colorid and confidence > confidencetrshold:
            print("+   [Correct bin] Pixelcount has choosen '" + str(bestcolorbin.color.colorname) + "' (" + str(bestcolorbin.color.colorid) + ") with confidence " + str(confidence) + "%")
            pixelsuccess += 1
        elif confidence < confidencetrshold:
            print("-   [No Match] Pixelcount search has a confidence of " + str(confidence) +  ". Had found '"  + str(bestcolorbin.color.colorname) + "' (" + str(bestcolorbin.color.colorid) + ")")
            pixelnoresult += 1
        elif confidence > confidencetrshold:
            pixelfalsep += 1 
            print("--  [False positive] Pixelcount has choosen bin '" + str(bestcolorbin.color.colorname) + "' (" + str(bestcolorbin.color.colorid) +") with confidence " + str(confidence) + "%")

    if combinesearch:
        print("Combined Search")
        if bestcolorbin.color.colorid == avgcolorid:
            chosenid = bestcolorbin.color.colorid
        elif avgcolorid > 0:
            chosenid = avgcolorid
        else:
            chosenid = 0
            copmbinedfailure += 1
            print("-   [No Match] Combined search has nothing to offer. ")

        if pathsandcolorid["color_id"] == chosenid and chosenid != 0:
            print("+   [Correct bin] Combined search has choosen " + str(bestcolorbin.color.colorname) + " id: " + str(bestcolorbin.color.colorid))
            combinedsuccess += 1
        elif chosenid != 0:
            combinedfalsep += 1 
            print("--  [False positive] Combined search has choosen bin " + str(bestcolorbin.color.colorname) + " id: " + str(bestcolorbin.color.colorid))
    
    key = cv2.waitKey(0)
    if key == ord('q'):
        masking = False
        break
    
    if key == ord('s'):
        print("s pressed")
        img_name = "should_be_{}.png".format(pathsandcolorid["color_name"])
        cv2.imwrite(img_name, img)
        print("{} written!".format(img_name))

if dominantsearch:
    print("Dom Color Search proccessed " + str(total) + " images. " + str(dsuccess) + " with success (" + str(int(dsuccess/total*100)) + "%) and " + str(dfailure) + " unknown (" + str(int(dfailure/total*100)) + "%) including " + str(dfalsep) + " False positives (" + str(int(dfalsep/total*100)) + "%)." )
if avgsearch:
    print("AVG Color proccessed " + str(total) + " images. " + str(avgsuccess) + " with success (" + str(int(avgsuccess/total*100)) + "%) and " + str(avgfailure) + " unknown (" + str(int(avgfailure/total*100)) + "%) including " + str(avgfalsep) + " False positives (" + str(int(avgfalsep/total*100)) + "%)." )
if pixelcountsearch:
    print("Pixelsearch proccessed " + str(total) + " images. " + str(pixelsuccess) + " with success (" + str(int(pixelsuccess/total*100)) + "%) and " + str(pixelnoresult) + " unknown (" + str(int(pixelnoresult/total*100)) + "%) including " + str(pixelfalsep) + " False positives (" + str(int(pixelfalsep/total*100)) + "%). " )
if combinesearch:
    print("combinesearch proccessed " + str(total) + " images. " + str(combinedsuccess) + " with success (" + str(int(combinedsuccess/total*100)) + "%) and " + str(copmbinedfailure) + " unknown (" + str(int(copmbinedfailure/total*100)) + "%) including " + str(combinedfalsep) + " False positives (" + str(int(combinedfalsep/total*100)) + "%)." )