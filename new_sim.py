import numpy as np
import os
import time


class roadModel():
    ''' A model for road with lanes'''

    def __init__(self, road_length=20, lane=5):
        self.road_length = road_length
        self.lane = lane
        self.road = np.zeros(
            (self.road_length, self.lane), dtype='float')

    def updateRoad(self,car):
        self.road[car.x,car.y] = car.speed

    def displayRoad(self):
        print '-'*80
        print self.road    
        print '-'*80

class car():
    def __init__(self,newRoad):
        self.x = 10     
        self.y = np.random.randint(0,newRoad.lane)
        self.speed = 50.0

if __name__ == '__main__':
   newRoad = roadModel()
   newRoad.displayRoad()
   agent_car = car(newRoad)
   newRoad.updateRoad(agent_car)             
   newRoad.displayRoad()
                    
