import numpy as np
# the following congic can possibly change according to season
# For example the date can be get and season be specified. Then If season == 'Winter' :  -----> Config= {}


Config = {
   'fuzzy': {
        'range': {
            'serverroom_temperature': np.arange(20, 45, 1),
            'softwareroom_temperature': np.arange(18, 38, 1),
            'serverroom_humidity': np.arange(6, 66, 1),

            'cooler': np.arange(0, 15, 1)
        },
        'membership_function': {
            'serverroom_temperature': {
                'cold': [20, 25, 30],
                'mild': [25, 30, 35],
                'warm': [30, 35, 40],
                'hot': [35, 40, 45]
            },
            'softwareroom_temperature': {
                'cold': [18, 22, 26],
                'mild': [22, 26, 30],
                'warm': [26, 30, 34],
                'hot': [30, 34, 38]
            },

            'serverroom_humidity': {
                'low': [6, 18, 30],
                'normal': [18, 30, 42],
                'high': [30, 42, 54],
                'very_high': [42, 54, 66]
            },


            'cooler': {
                'zero': [0, 0, 0],
                'low': [0, 4, 8],
                'medium': [6, 8, 10],
                'high': [8, 10, 12]
            }
        }
    }
}
