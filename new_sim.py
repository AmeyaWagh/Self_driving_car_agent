import numpy as np
import os
import time


class roadModel():
    ''' A model for road with lanes '''

    def __init__(self, road_length=20, lane=5):
        self.road_length = road_length
        self.lane = lane
        self.road = np.zeros(
            (self.road_length, self.lane), dtype='float')

    def updateRoad(self, agentCar, trafficCarsList):
        ''' Updates the road matrix '''
        self.road[:, :] = 0
        self.road[agentCar.x, agentCar.y] = agentCar.speed
        for everyCar in trafficCarsList:
            self.road[everyCar.x, everyCar.y] = everyCar.speed

    def displayRoad(self):
        ''' Print the road matrix on stdout '''
        os.system('clear')
        print '-'*80
        print self.road
        print '-'*80


class agent_car():

    def __init__(self, roadInstance, speed=50.0, maxSpeed=100.0):
        self.roadInst = roadInstance
        self.x = 10
        self.y = np.random.randint(0, self.roadInst.lane)
        self.speed = speed
        self.maxSpeed = maxSpeed


class traffic_car():

    def __init__(self, roadInstance, maxSpeed=100.0):
        self.roadInst = roadInstance
        self.x = roadInstance.road_length-1
        self.y = np.random.randint(0, self.roadInst.lane)
        self.speed = 10.0*np.random.randint(1, 10)
        self.maxSpeed = maxSpeed

    def iterate(self, iteration):

        # if there is car in front, move aside
        if self.roadInst.road[self.x-1, self.y] > 0:

            # check if you have lanes free to change
            # car cannot go left if in lane 0 and right if in lane 4
            if self.y in range(1, self.roadInst.lane-1):
                if self.roadInst.road[self.x, self.y-1] == 0:
                    self.y -= 1
                elif self.roadInst.road[self.x, self.y+1] == 0:
                    self.y += 1
            elif (self.y==0) and (self.roadInst.road[self.x, self.y+1] == 0):        
                self.y += 1
            elif (self.y==(self.roadInst.lane-1)) and (self.roadInst.road[self.x, self.y-1] == 0):        
                self.y -= 1
            
            else:
                # wait for room and change lane later
                pass

        else:
            if(self.x > 0):
                if (iteration % int((self.maxSpeed-self.speed)/10.0) == 0):
                    self.x -= 1
            else:
                self.speed = 0


class trafficModel():

    def __init__(self, traffic_car, roadInstance, space_bet_vehicles=3):
        self.CarsList = []
        self.roadInstance = roadInstance
        self.traffic_car = traffic_car
        self.space_bet_vehicles = space_bet_vehicles
        self.carsPassed = 0

    def updateTraffic(self, iteration):
        if len(self.CarsList) == 0:
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        if (iteration % self.space_bet_vehicles == 0):
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        for everyCar in self.CarsList:
            if everyCar.speed == 0:
                self.CarsList.pop(
                    self.CarsList.index(everyCar))

            lastPos = everyCar.x

            everyCar.iterate(iteration)

            currPos = everyCar.x

            if (lastPos == 10) and (currPos == 9):
                self.carsPassed -= 1

            elif (lastPos == 9) and (currPos == 10):
                self.carsPassed += 1


class environment():

    def __init__(self):
        pass
#--------------------------------------------------#

if __name__ == '__main__':
    newRoad = roadModel()
    agentCar = agent_car(newRoad)
    traffic = trafficModel(traffic_car, newRoad)
    iteration = 0

    while(1):
        time.sleep(0.5)
        newRoad.updateRoad(agentCar, traffic.CarsList)
        traffic.updateTraffic(iteration)
        newRoad.displayRoad()
        print "iteration", iteration
        print "carsPassed", traffic.carsPassed
        iteration += 1
        # print "trafficCars",traffic.CarsList
