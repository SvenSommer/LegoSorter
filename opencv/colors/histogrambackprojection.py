import cv2
import numpy as np
import pymysql

connection = pymysql.connect(host="localhost",    # your host, usually localhost
                        user="WebDBUser",         # your username
                        passwd="qF2J%9a84zU",  # your password
                        db="LegoSorterDB")        # name of the data base

cursor = connection.cursor(pymysql.cursors.DictCursor)

def loadimagepathsfromDB(runid, limit):
    global connection, cursor
    sql = """SELECT pi.path, rp.color_id, c.color_name FROM LegoSorterDB.Recognisedparts rp
                LEFT JOIN LegoSorterDB.Recognisedimages ri ON rp.id = ri.part_id
                LEFT JOIN LegoSorterDB.Partimages pi ON ri.image_id = pi.id
                LEFT JOIN LegoSorterDB.Colors c ON rp.color_id = c.color_id
                WHERE rp.color_id > 0
                AND rp.deleted IS NULL 
                AND pi.deleted IS NULL
                AND pi.camera = 'USB'
                AND rp.run_id = """ + str(runid) + """
                AND ri.score > 0 LIMIT """ + str(limit)
    cursor.execute(sql)
    pathsandcolorids = cursor.fetchall()
    return pathsandcolorids 

def nothing(*arg):
    pass

def CropFromCenter(image, margin):
    height, width = image.shape[:2]
    m = margin
    cx = width / 2
    cy = height / 2
    upper_left = (int(cx - m*width*0.01), int(cy - m*height*0.01))
    bottom_right = (int(cx + m), int(cy + m))
    rect_img = image[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
    return rect_img



cv2.namedWindow('HistogramBackprojection')
#cv2.setMouseCallback('RGB', onMouse)
cv2.createTrackbar('Crop margin', 'HistogramBackprojection', 2, 40, nothing)
cv2.createTrackbar('lower treshold', 'HistogramBackprojection', 1, 255, nothing)
cv2.createTrackbar('upper treshold', 'HistogramBackprojection', 1, 255, nothing)
cv2.setTrackbarPos('Crop margin', 'HistogramBackprojection', 11)
cv2.setTrackbarPos('lower treshold', 'HistogramBackprojection', 94)
cv2.setTrackbarPos('upper treshold', 'HistogramBackprojection', 255)

pathsandcolorids = loadimagepathsfromDB(9,1000)  
for pathsandcolorid in pathsandcolorids:
    while True:
        target = cv2.imread(pathsandcolorid["path"])
        #cv2.imshow("HistogramBackprojection",target )
        hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
        cropMargin = cv2.getTrackbarPos('Crop margin', 'HistogramBackprojection')
        lower_treshold = cv2.getTrackbarPos('lower treshold', 'HistogramBackprojection')
        upper_treshold = cv2.getTrackbarPos('upper treshold', 'HistogramBackprojection')
        #print("cropMargin: " + str(cropMargin))
        roi = CropFromCenter(target, cropMargin)
        cv2.imshow("HistogramBackprojection_roi",roi)
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
        ret,thresh = cv2.threshold(dst,lower_treshold,upper_treshold,0)
        thresh = cv2.merge((thresh,thresh,thresh))
        res = cv2.bitwise_and(target,thresh)

        #res = np.vstack((target,thresh,res))
        cv2.imshow('HistogramBackprojection',res)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break