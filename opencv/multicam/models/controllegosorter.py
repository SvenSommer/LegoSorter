import time
from datetime import datetime

class Controllegosorter:
    def __init__(self, session):
        self.session = session
        self.lifterControllerIp = "http://192.168.178.71"
        self.vibrationControllerIp = "http://192.168.178.70"
        self.conveyorControllerIp = "http://192.168.178.72"
        self.valveControllerIps = {
                                    "1":"http://192.168.178.86",
                                    "2":"http://192.168.178.106",
                                    "3":"http://192.168.178.100", 
                                    "4":"http://192.168.178.102"
        }
        self.scaleControllerIps = {
                                    "1":"http://192.168.178.84",
                                    "2":"http://192.168.178.87",
                                    "3":"http://192.168.178.98", 
                                    "4":"http://192.168.178.92",
                                    "5":"http://192.168.178.76", 
                                    "6":"http://192.168.178.95",
                                    "7":"http://192.168.178.77",
                                    "8":"http://192.168.178.101",
                                    "9":"http://192.168.178.115",
                                    "10":"http://192.168.178.111",
                                    "11":"http://192.168.178.117",
                                    "12":"http://192.168.178.74",
                                    "13":"http://192.168.178.85",
                                    "14":"http://192.168.178.105",
                                    "15":"http://192.168.178.88",
                                    "16":"http://192.168.178.103",
                                    "17":"http://192.168.178.91",
                                    "18":"http://192.168.178.107",
                                    "19":"http://192.168.178.79",
                                    "20":"http://192.168.178.112",
                                    "21":"http://192.168.178.93",
                                    "22":"http://192.168.178.90",
                                    "23":"http://192.168.178.89",
                                    "24":"http://192.168.178.108",
                                    "25":"http://192.168.178.96",
                                    "26":"http://192.168.178.109",
                                    "27":"http://192.168.178.97"
                                    }

    def startConveyor(self, speedconveyor = 29):
        self.session.put(self.conveyorControllerIp + '/update?clientmode=SCRIPT&motormode=ON&speed=' + str(speedconveyor))

    def startLegoSorter(self, speedconveyor = 29, speedvibration = 20, speedlifter = 35):
        self.session.put(self.conveyorControllerIp + '/update?clientmode=AUTO&motormode=ON&speed=' + str(speedconveyor))
        self.session.put(self.vibrationControllerIp + '/update?clientmode=AUTO&motormode=ON&speed=' + str(speedvibration))
        self.session.put(self.lifterControllerIp + '/update?clientmode=SCRIPT&motormode=ON&speed='+  str(speedlifter))

    def stopLegoSorter(self, time=2.0):
        self.session.put(self.lifterControllerIp + '/update?clientmode=SCRIPT&motormode=OFF')
        self.session.put(self.vibrationControllerIp + '/update?clientmode=SCRIPT&motormode=OFF')
        self.session.put(self.conveyorControllerIp + '/update?clientmode=SCRIPT&motormode=OFF')

    def haltSupplyChain(self):
        self.session.put(self.lifterControllerIp + '/update?clientmode=Pause&motormode=OFF')
        self.session.put(self.vibrationControllerIp + '/update?clientmode=Pause&motormode=OFF')


    def resumeLegoSorter(self):
        self.session.put(self.lifterControllerIp + '/update?clientmode=SCRIPT&motormode=ON')
        self.session.put(self.vibrationControllerIp + '/update?clientmode=SCRIPT&motormode=ON')
        self.session.put(self.conveyorControllerIp + 'update?clientmode=SCRIPT&motormode=ON')

    def resumeSupplyChain(self):
        self.session.put(self.lifterControllerIp + '/update?clientmode=SCRIPT&motormode=ON')
        self.session.put(self.vibrationControllerIp + '/update?clientmode=SCRIPT&motormode=ON')


    def pushBrick(self, partid, bucketnumber, pushtime, weight, duration=400) :
        request_address = self.valveControllerIps["1"]
        bucketnumberForValveController = bucketnumber
        if (bucketnumber > 8 and bucketnumber < 17) :
            request_address = self.valveControllerIps["2"]
            bucketnumberForValveController =  bucketnumber - 8
        elif (bucketnumber > 16 and bucketnumber < 25) :
            request_address = self.valveControllerIps["3"]
            bucketnumberForValveController =  bucketnumber - 16
        elif (bucketnumber > 24 and bucketnumber < 29) :
            request_address = self.vvalveControllerIps["4"]
            bucketnumberForValveController =  bucketnumber - 24

        print("pushBrickRequest| partid: " +str(partid) + "\tbucketnumber: " + str(bucketnumber) + "\tpushtime: " + str(pushtime) + "\tweight: " + str(weight)+ "\tduration: " + str(duration))
        requesttext = request_address + '/pushBrick?time=' + str(pushtime) + '&bucket=' + str(bucketnumberForValveController) + '&duration=' + str(duration)
        print(f"{datetime.now()} {partid} {requesttext}")
        self.session.put(requesttext)
        self.session.put(self.scaleControllerIps[str(bucketnumber)] + '/exspectBrick?time='+ str(pushtime) +'&weight=' + str(weight) + '&brickId=' + str(partid))