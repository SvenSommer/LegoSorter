import requests

def stopLegoSorter():
	requests.put('http://liftercontroller/update?clientmode=HALT&motormode=OFF&speed=15')
	requests.put('http://vibrationcontroller/update?clientmode=HALT&motormode=OFF&speed=20')
	requests.put('http://conveyorcontroller/update?clientmode=HALT&motormode=OFF&speed=40')

stopLegoSorter()