import os
import pickle
import numpy as np
class MainModel:
    def __init__(self):
        pass

    def __process__(self, data):
        base_path = os.path.join('model', data['car'])

        model_path = os.path.join(base_path, data['model'])
        x_path = os.path.join(base_path, 'scaler_x.pkl')
        y_path = os.path.join(base_path, 'scaler_y.pkl')

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

        return model_path, x_path, y_path, numpy_array

    def __transform_data__(self, data, x_path):
        with open(x_path, 'rb') as file:
            scaler_x = pickle.load(file)
            input = np.array([data, data])

            return scaler_x.transform(input)
        
    def predict(self, data) -> float:
        pathFile, x_path, y_path, cleanData = self.__process__(data)
        cleanData = self.__transform_data__(cleanData, x_path)
        print('iam here')
        try:
            with open(pathFile, 'rb') as file:
                model = pickle.load(file) 
                print('iam predict 0000000')

                raw_prediction = model.predict(cleanData)[0, 0]

                print(raw_prediction)
            
            with open(y_path, 'rb') as file:
                print('iam scale 000000')

                scaler_y = pickle.load(file)
                tdv = scaler_y.inverse_transform(np.array(raw_prediction).reshape(-1, 1))
                
                print('iam scale 11111')
               
            return round(tdv[0,0], 4)

        except Exception as e:
            print(e)
            return -1