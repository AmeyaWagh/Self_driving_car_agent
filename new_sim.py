import numpy as np
import os
import time
import random
import traceback


class environmentException(Exception):
    ''' class to handle exceptions of environment to avoid breaking of code '''
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return error


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
    ''' models an agent car '''

    def __init__(self, roadInstance, speed=50.0, maxSpeed=100.0):
        self.roadInst = roadInstance
        self.x = 10
        self.y = np.random.randint(0, self.roadInst.lane)
        self.speed = speed
        self.maxSpeed = maxSpeed

    def steering(self, direction):
        ''' steer car to switch lane '''
        if direction not in ['Left', 'Right']:
            raise environmentException(
                "action space has only 'Left' and 'Right' as inputs")

        if (direction == 'Left') and (self.y > 0):
            # IsLeftLaneEmpty
            if (self.roadInst.road[self.x, self.y-1] == 0):
                self.y -= 1
        elif (direction == 'Right') and (self.y < (self.roadInst.lane-1)):
            # IsRightLaneEmpty
            if (self.roadInst.road[self.x, self.y+1] == 0):
                self.y += 1
        else:
            pass


class traffic_car():
    ''' models an traffic car '''

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
                IsLeftLaneEmpty = (self.roadInst.road[self.x, self.y-1] == 0)
                IsRightLaneEmpty = (self.roadInst.road[self.x, self.y+1] == 0)

                if IsLeftLaneEmpty and IsRightLaneEmpty:
                    self.y += [-1, 1][random.randint(0, 1)]
                elif IsLeftLaneEmpty:
                    self.y -= 1
                elif IsRightLaneEmpty:
                    self.y += 1

            elif (self.y == 0) and (self.roadInst.road[self.x, self.y+1] == 0):
                self.y += 1
            elif (self.y == (self.roadInst.lane-1)) and (
                    self.roadInst.road[self.x, self.y-1] == 0):
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
    ''' Single way multi-lane traffic model '''

    def __init__(self, traffic_car, roadInstance, space_bet_vehicles=3):
        self.CarsList = []
        self.roadInstance = roadInstance
        self.traffic_car = traffic_car
        self.space_bet_vehicles = space_bet_vehicles
        self.carsPassed = 0

    def updateTraffic(self, iteration):

        # if there is no car in queue, add traffic car
        if len(self.CarsList) == 0:
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        if (iteration % self.space_bet_vehicles == 0):
            self.CarsList.append(
                self.traffic_car(self.roadInstance))

        # if the car has passed the simulator window, remove instance from list
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
    ''' openAI gym like environment '''

    def __init__(self):
        newRoad = roadModel()
        agentCar = agent_car(newRoad)
        traffic = trafficModel(traffic_car, newRoad)
        iteration = 0
        self.done = False

    def reset(self):
        pass

    def observation(self):
        pass

    def reward(self):
        return traffic.carsPassed

    def done(self):
        return self.done

    def info(self):
        return {'info': 'some info'}


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
        # try:
        #     agentCar.steering(['Left','Right'][random.randint(0,1)])
        # except:
        #         traceback.print_exc()
        #         print "Game Over"
        #         exit()
        print "iteration", iteration
        print "carsPassed", traffic.carsPassed
        iteration += 1
        # print "trafficCars",traffic.CarsList
