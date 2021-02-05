class Colorbin(object):
     def __init__(self, color):
         self.color = color
         self.lower_treshold = color.lower_treshold
         self.upper_treshold = color.upper_treshold
         self.count = 0
