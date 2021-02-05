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
         self.hls = rgb2hls(self.rgb)

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
        print(legocolor.colorname  + ", hex: " + str(legocolor.hex) + ", rgb "+ str(legocolor.rgb) + ",hsv " + str(legocolor.hsv)+ ",hsl " + str(legocolor.hls)) 
        returnColors.append(legocolor)

    return returnColors



def main():
    legocolors = getColorsFromDB()
    for color in legocolors:
        plt.scatter(color.hls[0], color.hls[2], color=downscaleColorValues(color.rgb))

    #plt.scatter(30,180, s=50,marker='x')
    plt.xlabel("hue")
    plt.ylabel("saturation")
    plt.show()

    for color in legocolors:
        plt.scatter(color.hls[2], color.hls[1], color=downscaleColorValues(color.rgb))
    plt.xlabel("saturation")
    plt.ylabel("luminance")
    plt.show()


main()