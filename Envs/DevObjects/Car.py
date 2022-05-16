#Kyle R Fogerty

from random import randint

class Car:
    def getEndPoint(self, lanes):
        lanes_index = []
        lane_index = 0
        for lane in lanes:
            for i in range(0, lane):
                lanes_index.append(0)
            lane_index += 1
        sum_of_lanes = sum(lanes)
        final_lane = randint(0, sum_of_lanes-1)
        final_street = lanes_index[final_lane]
        lane_index = randint(0, lanes[final_street]-1)
        return final_street, lane_index

    def __init__(self, start_street: int, lanes: list):
        self.number_of_streets = len(lanes)
        self.start_street = start_street
        self.start_lane = randint(0, lanes[self.start_street]-1)
        self.final_street, self.final_lane = self.getEndPoint(lanes)
    
    def getStart(self):
        return [self.start_street, self.start_lane]
    
    def getDestination(self):
        return self.final_street, self.final_lane