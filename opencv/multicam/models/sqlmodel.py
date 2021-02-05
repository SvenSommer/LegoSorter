import pymysql
import os
import time

class SQLModel:
    def __init__(self, runid):
        self.connection = pymysql.connect(host="localhost",    # your host, usually localhost
                     user="WebDBUser",         # your username
                     passwd="qF2J%9a84zU",  # your password
                     db="LegoSorterDB") 
        self.cursor = self.connection.cursor()
        self.runid = runid

    def InsertIntoPartimages(self, filename,image, ts):
        size = os.path.getsize(filename)
        imported = ts.strftime('%Y-%m-%d %H:%M:%S')
        created = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `Partimages` (`run_id`, `path`, `size_kb`, `x`, `y`, `w`, `h`, `color`, `camera`, `created`, `imported`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (self.runid, filename, size, int(image.x), int(image.y), int(image.w), int(image.h), str(image.color), str(image.camera), created, imported))
        self.connection.commit()

        return self.cursor.lastrowid

    def InsertIntoRecognisedParts(self):
        created = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `Recognisedparts` (`run_id`,`created`) VALUES (%s,%s)"
        self.cursor.execute(sql, (self.runid, created))
        self.connection.commit()

        return self.cursor.lastrowid

    def InsertIntoRecognisedImages(self, partid, imageid):
        created = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO `Recognisedimages` (`part_id`,`image_id`,`created`) VALUES (%s,%s,%s)"
        self.cursor.execute(sql, (partid, imageid, created))
        self.connection.commit()