def buildPathLayer(self):
    self.sizeLayers()
    full_layer = []
    for x in range(0, (self.x_len)):
        temp_col = []
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

def displayPathLayer(x_len, y_len, intersection_seed):
    full_layer = []
    for x in range(0, (x_len)):
        temp_col = []
        for y in range(0, (y_len)):
            if x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0] \
                and y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                temp_col.append(0)
            elif x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0] \
                or y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                temp_col.append(1)
            else:
                temp_col.append(-1)
        full_layer.append(temp_col)
    for layer in full_layer:
        print(layer)

def displayLightLayer(x_len, y_len, intersection_seed, streets):
        full_layer = []
        for x in range(0, (x_len)):
            temp_col = []
            for y in range(0, (y_len)):
                if x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0] \
                    and y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                    temp_col.append(0)
                elif x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0]:
                    temp_col.append(streets[1].light_status)
                elif y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                    temp_col.append(streets[0].light_status)
                else:
                    temp_col.append(0)
            full_layer.append(temp_col)
        for layer in full_layer:
            print(layer)

def displayCarLayer(x_len, y_len, intersection_seed, streets):
        full_layer = []
        for x in range(0, (x_len)):
            temp_col = []
            for y in range(0, (y_len)):
                if x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0] \
                    and y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                    temp_col.append(0)
                elif x >= intersection_seed[0][1] and x < intersection_seed[0][1] + intersection_seed[1][0]:
                    #Hor
                    if y < intersection_seed[1][1]:
                        #Pre
                        index = x - intersection_seed[0][1]
                        if streets[1].lanes[index].pre_light[y] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                    else:
                        #post
                        index = x - intersection_seed[0][1]
                        index_1 = y - (intersection_seed[1][1] + intersection_seed[0][0])
                        if streets[1].lanes[index].post_light[index_1] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                elif y >= intersection_seed[1][1] and y < intersection_seed[1][1] + intersection_seed[0][0]:
                    if x < intersection_seed[0][1]:
                        #Pre 
                        index = y - intersection_seed[1][1]
                        if streets[0].lanes[index].pre_light[x] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                    else:
                        index = y - intersection_seed[1][1]
                        index_1 = x - (intersection_seed[0][1] + intersection_seed[1][0])
                        if streets[0].lanes[index].post_light[index_1] == None:
                            temp_col.append(0)
                        else:
                            temp_col.append(1)
                        
                else:
                    temp_col.append(0)
            full_layer.append(temp_col)
        for layer in full_layer:
            print(layer)