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

    def updateRoad(self, agentCar, trafficCarsList):
        self.road[:, :] = 0
        self.road[agentCar.x, agentCar.y] = agentCar.speed
        for everyCar in trafficCarsList:
            self.road[everyCar.x, everyCar.y] = everyCar.speed

    def displayRoad(self):
        os.system('clear')
        print '-'*80
        print self.road
        print '-'*80


class agent_car():

    def __init__(self, roadInstance):
        self.road = roadInstance
        self.x = 10
        self.y = np.random.randint(0, self.road.lane)
        self.speed = 50.0


class traffic_car():

    def __init__(self, roadInstance):
        self.road = roadInstance
        self.x = roadInstance.road_length-1
        self.y = np.random.randint(0, self.road.lane)
        self.speed = 50.0

    def iterate(self):
        if(self.x > 0):
            self.x -= 1
        else:
            self.speed = 0


class trafficModel():

    def __init__(self,traffic_car,roadInstance,space_bet_vehicles=3):
        self.CarsList = []
        self.roadInstance = roadInstance
        self.traffic_car = traffic_car
        self.space_bet_vehicles=space_bet_vehicles

    def updateTraffic(self,iteration):
        if len(self.CarsList)==0:
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        if (iteration % self.space_bet_vehicles == 0):
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        for everyCar in self.CarsList:
            if everyCar.speed == 0:
                self.CarsList.pop(
                    self.CarsList.index(everyCar))
            everyCar.iterate()                
    


#--------------------------------------------------#

if __name__ == '__main__':
    newRoad = roadModel()
    # newRoad.displayRoad()
    agentCar = agent_car(newRoad)
    # trafficCar = traffic_car(newRoad)
    traffic = trafficModel(traffic_car,newRoad)
    iteration = 0

    while(1):
        time.sleep(0.5)
        newRoad.updateRoad(agentCar, traffic.CarsList)
        traffic.updateTraffic(iteration)
        # newRoad.updateRoad(trafficCar)
        # trafficCar.iterate()
        newRoad.displayRoad()
        print "iteration", iteration
        iteration += 1
        print "trafficCars",traffic.CarsList
