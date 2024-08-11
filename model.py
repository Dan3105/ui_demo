import os
import pickle
import numpy as np
class MainModel:
    def __init__(self):
        pass

    def __process__(self, data) -> dict:
        pathFile = os.path.join('model', data['car'], data['model']),
        numpy_array = np.array([
            max(data['quantity(kWh)'], 0),
            int(data['city']),
            int(data['motor_way']),
            int(data['country_roads']),
            int(data['A/C']),
            int(data['park_heating']),
            max(data['avg_speed(km/h)'], 0),
            data['encoded_driving_style'],
            data['encoded_tire_type'],
            1 if data['ecr_dev_type'] >= 0 else 0
        ])

        return pathFile, numpy_array

    def __transform_data__(self, data):
        return data

    def predict(self, data) -> float:
        pathFile, cleanData = self.__process__(data)
        cleanData = self.__transform_data__(cleanData)
        try:
            with open(pathFile[0], 'rb') as file:
                model = pickle.load(file) 
                input = np.expand_dims(cleanData, 0) #dim (1, n)
                return round(model.predict(input)[0,0], 4) #
        except Exception as e:
            print(e)
            return -1