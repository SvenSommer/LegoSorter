import json

class PredictController:
    def __init__(self, session):
        self.session = session

    def predictPartno(self, imagepath):
        request = self.session.post('http://192.168.178.46:3000/predict', json={"imagepath":imagepath})
        return request