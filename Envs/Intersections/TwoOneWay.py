import os
import sys
sys.path.insert(1, os.getcwd())

from Envs.Intersections.DisplayLayer import displayCarLayer, displayLightLayer, displayPathLayer
from Envs.DevObjects.Car import Car
import numpy as np
from random import randint
import copy

class Intersection:
    def sizeLayers(self):
        self.x_len = (self.intersection_seed[0][1] * 2) + self.intersection_seed[1][0]
        self.y_len = (self.intersection_seed[1][1] * 2) + self.intersection_seed[0][0]
    
    def buildPathLayer(self):
        self.sizeLayers()
        full_layer = []
        for x in range(0, (self.x_len)):
            temp_col =[]
            for y in range(0, (self.y_len)):
                if x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0] \
                    and y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    temp_col.append(0)
                elif x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0] \
                    or y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    temp_col.append(1)
                else:
                    temp_col.append(-1)
            full_layer.append(temp_col)
        self.path_layer = full_layer
     
    
    def buildCarLayer(self):
        full_layer = []
        for x in range(0, (self.x_len)):
            temp_col = []
            for y in range(0, (self.y_len)):
                if x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0] \
                    and y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    temp_col.append(0)
                elif x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0]:
                    #Hor
                    if y < self.intersection_seed[1][1]:
                        #Pre
                        index = x - self.intersection_seed[0][1]
                        if self.streets[1].lanes[index].pre_light[y] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                    else:
                        #post
                        index = x - self.intersection_seed[0][1]
                        index_1 = y - (self.intersection_seed[1][1] + self.intersection_seed[0][0])
                        if self.streets[1].lanes[index].post_light[index_1] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                elif y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    if x < self.intersection_seed[0][1]:
                        #Pre 
                        index = y - self.intersection_seed[1][1]
                        if self.streets[0].lanes[index].pre_light[x] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                    else:
                        index = y - self.intersection_seed[1][1]
                        index_1 = x - (self.intersection_seed[0][1] + self.intersection_seed[1][0])
                        if self.streets[0].lanes[index].post_light[index_1] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                        
                else:
                    temp_col.append(0)
            full_layer.append(temp_col)
        self.cars_layer = full_layer
    
    def buildLightLayer(self):
        full_layer = []
        for x in range(0, (self.x_len)):
            temp_col = []
            for y in range(0, (self.y_len)):
                if x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0] \
                    and y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    temp_col.append(0)
                elif x >= self.intersection_seed[0][1] and x < self.intersection_seed[0][1] + self.intersection_seed[1][0]:
                    temp_col.append(self.streets[1].light_status)
                elif y >= self.intersection_seed[1][1] and y < self.intersection_seed[1][1] + self.intersection_seed[0][0]:
                    temp_col.append(self.streets[0].light_status)
                else:
                    temp_col.append(0)
            full_layer.append(temp_col)
        self.lights_layer = full_layer
    
    def displayPathLayer(self):
        displayPathLayer(self.x_len, self.x_len, self.intersection_seed)
    
    def displayCarLayer(self):
        displayCarLayer(self.x_len, self.x_len, self.intersection_seed, self.streets)
    
    def displayLightLayer(self):
        displayLightLayer(self.x_len, self.x_len, self.intersection_seed, self.streets)

    def getObservation(self):
        observation = []
        self.buildPathLayer()
        self.buildCarLayer()
        self.buildLightLayer()
        observation.append(self.lights_layer)
        observation.append(self.cars_layer)
        observation.append(self.path_layer)
        return np.array(observation)

    def __init__(self, intersection_seed: list):
        self.prev_action = None
        self.intersection_seed = intersection_seed
        #Streets
        self.streets = []
        for street in self.intersection_seed:
            self.streets.append(Intersection.Street(*street, self))
        #Scoring Features
        self.score = 0.0
        self.done = False
        #ML Setup Features
        self.actions = len(self.intersection_seed) - 1
        self.buildPathLayer()
        self.buildCarLayer()
        self.buildLightLayer()
        self.observation_space = self.getObservation()
    
    def reset(self):
        self.prev_action = None
        #Streets
        self.streets = []
        for street in self.intersection_seed:
            self.streets.append(Intersection.Street(*street, self))
        #Scoring Features
        self.score = 0.0
        self.done = False
        return self.getObservation()
        
    
    #Street Class Which Contains The Light Status and all the lanes
    class Street:
        def __init__(self, number_of_lanes: int, length_of_street: int, light_status: int, intersection):
            #Setup Values
            self.number_of_lanes = number_of_lanes
            self.length_of_street = length_of_street
            self.light_status = light_status
            #Self Values
            self.intersection = intersection
            #Lanes
            self.lanes = []
            for _ in range(0, self.number_of_lanes):
                self.lanes.append(Intersection.Street.Lane(length_of_street, self.intersection, self))
        
        def moveStreet1(self):
            for lane in self.lanes:
                lane.moveLane1()
        
        def moveStreet2(self):
            for lane in self.lanes:
                lane.moveLane2()

        class Lane:
            def __init__(self, lane_length: int, intersection, street):
                self.pre_light = [None for _ in range(0, lane_length)]
                self.post_light = [None for _ in range(0, lane_length)]
                self.intersection = intersection
                self.street = street
                self.wait = 1
            
            def movePost(self):
                if self.street.light_status == 1:
                    if self.post_light[0] != None:
                        #Check if spot open
                        self.post_light.pop(0)
                        self.post_light.append(None)
                        self.intersection.score += 2
                        return
                    else:
                        self.post_light.pop(0)
                        self.post_light.append(None)
                else:
                    if self.post_light[0] == None:
                        self.post_light.pop(0)
                        self.post_light.append(None)
            
            def movePre(self):
                if self.street.light_status == 1:
                    if self.pre_light[0] != None:
                        #Check if spot open
                        dest_street, dest_lane = self.pre_light[0].getDestination()
                        if self.intersection.streets[dest_street].lanes[dest_lane].post_light[-1] == None:
                            car = self.pre_light.pop(0)
                            self.pre_light.append(None)
                            self.intersection.score += 1
                            self.intersection.streets[dest_street].lanes[dest_lane].post_light[-1] = car
                            self.wait = 1
                        else:
                            self.intersection.score -= (1 * self.wait)
                            self.wait += 1
                    else:
                        self.pre_light.pop(0)
                        self.pre_light.append(None)
                        self.wait = 1
                else:
                    if self.pre_light[0] == None:
                        self.pre_light.pop(0)
                        self.pre_light.append(None)
                        self.wait = 1
                    else:
                        self.wait += 1

            def moveLane1(self):
                self.movePost()
            
            def moveLane2(self):
                self.movePost()


    def updateLights(self, action):
        for street in self.streets:
            street.light_status = -1
        if self.prev_action == action:
            self.streets[action].light_status = 1
        else:
            self.prev_action = action
    
    def move(self):
        for street in self.streets:
            street.moveStreet1()
        for street in self.streets:
            street.moveStreet2()
    
    def addCars(self):
        amount = randint(0, 4)
        start_lane_streets = []
        while len(start_lane_streets) != amount:
            start = randint(0, 1)
            new_car = copy.deepcopy(Car(start, [3,1]))
            start_point = new_car.getStart()
            if start_point not in start_lane_streets:
                start_lane_streets.append(start_point)
                #Check If Avalible
                street_n = start_point[0]
                lane_n = start_point[1]
                if self.streets[street_n].lanes[lane_n].pre_light[-1] == None:
                    self.streets[street_n].lanes[lane_n].pre_light[-1] = new_car
                else:
                    self.done = True


    def step(self, action):
        self.score = 0
        self.updateLights(action)
        self.move()
        self.addCars()
        return self.getObservation(), self.score, self.done