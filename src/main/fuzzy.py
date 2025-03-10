from skfuzzy import control as ctrl
from .Config import Config
import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf

class Cooler_fan_fuzzy:
    def __init__(self):
        setting = Config

        #input    
        self.serverroom_temperature = {}
        self.serverroom_temperature['range'] = setting['fuzzy']['range']['serverroom_temperature']

        self.softwareroom_temperature = {}
        self.softwareroom_temperature['range'] = setting['fuzzy']['range']['softwareroom_temperature']


        self.serverroom_humidity = {}
        self.serverroom_humidity['range'] = setting['fuzzy']['range']['serverroom_humidity']

       
        #output
        self.cooler = {}
        self.cooler['range'] = setting['fuzzy']['range']['cooler']


        serverroom_temperature_mf = setting['fuzzy']['membership_function']['serverroom_temperature']
        self.serverroom_temperature['cold'] = mf.trimf(self.serverroom_temperature['range'],  serverroom_temperature_mf['cold']) 
        self.serverroom_temperature['mild'] = mf.trimf(self.serverroom_temperature['range'], serverroom_temperature_mf['mild'])
        self.serverroom_temperature['warm'] = mf.trimf(self.serverroom_temperature['range'], serverroom_temperature_mf['warm'])
        self.serverroom_temperature['hot'] = mf.trimf(self.serverroom_temperature['range'], serverroom_temperature_mf['hot'])

        softwareroom_temperature_mf = setting['fuzzy']['membership_function']['softwareroom_temperature']
        self.softwareroom_temperature['cold'] = mf.trimf(self.softwareroom_temperature['range'], softwareroom_temperature_mf['cold']) 
        self.softwareroom_temperature['mild'] = mf.trimf(self.softwareroom_temperature['range'], softwareroom_temperature_mf['mild'])
        self.softwareroom_temperature['warm'] = mf.trimf(self.softwareroom_temperature['range'], softwareroom_temperature_mf['warm'])
        self.softwareroom_temperature['hot'] = mf.trimf(self.softwareroom_temperature['range'], softwareroom_temperature_mf['hot'])

        serverroom_humidity_mf = setting['fuzzy']['membership_function']['serverroom_humidity']
        self.serverroom_humidity['low'] = mf.trimf(self.serverroom_humidity['range'], serverroom_humidity_mf['low']) 
        self.serverroom_humidity['normal'] = mf.trimf(self.serverroom_humidity['range'], serverroom_humidity_mf['normal'])
        self.serverroom_humidity['high'] = mf.trimf(self.serverroom_humidity['range'], serverroom_humidity_mf['high'])
        self.serverroom_humidity['very_high'] = mf.trimf(self.serverroom_humidity['range'], serverroom_humidity_mf['very_high'])

        cooler_mf = setting['fuzzy']['membership_function']['cooler']
        self.cooler['zero'] = mf.trimf(self.cooler['range'], cooler_mf['zero'])
        self.cooler['low'] = mf.trimf(self.cooler['range'], cooler_mf['low'])
        self.cooler['medium'] = mf.trimf(self.cooler['range'], cooler_mf['medium'])
        self.cooler['high'] = mf.trimf(self.cooler['range'], cooler_mf['high'])

    def compute_fan_speed(self, serverroom_temperature_input, softwareroom_temperature_input, serverroom_humidity_input):

        # setting = Config
        # serverroom_temperature_mf = setting['fuzzy']['membership_function']['serverroom_temperature']
        # if softwareroom_temperature_mf['cold'] >


        serverroom_temperature_level = {}
        serverroom_temperature_level['cold'] = fuzz.interp_membership(self.serverroom_temperature['range'], self.serverroom_temperature['cold'], serverroom_temperature_input)
        serverroom_temperature_level['mild'] = fuzz.interp_membership(self.serverroom_temperature['range'], self.serverroom_temperature['mild'], serverroom_temperature_input)
        serverroom_temperature_level['warm'] = fuzz.interp_membership(self.serverroom_temperature['range'], self.serverroom_temperature['warm'], serverroom_temperature_input)
        serverroom_temperature_level['hot'] = fuzz.interp_membership(self.serverroom_temperature['range'], self.serverroom_temperature['hot'], serverroom_temperature_input)

        softwareroom_temperature_level = {}
        softwareroom_temperature_level['cold'] = fuzz.interp_membership(self.softwareroom_temperature['range'], self.softwareroom_temperature['cold'], softwareroom_temperature_input)
        softwareroom_temperature_level['mild'] = fuzz.interp_membership(self.softwareroom_temperature['range'], self.softwareroom_temperature['mild'], softwareroom_temperature_input)
        softwareroom_temperature_level['warm'] = fuzz.interp_membership(self.softwareroom_temperature['range'], self.softwareroom_temperature['warm'], softwareroom_temperature_input)
        softwareroom_temperature_level['hot'] = fuzz.interp_membership(self.softwareroom_temperature['range'], self.softwareroom_temperature['hot'], softwareroom_temperature_input)

        serverroom_humidity_level = {}
        serverroom_humidity_level['low'] = fuzz.interp_membership(self.serverroom_humidity['range'], self.serverroom_humidity['low'], serverroom_humidity_input)
        serverroom_humidity_level['normal'] = fuzz.interp_membership(self.serverroom_humidity['range'], self.serverroom_humidity['normal'], serverroom_humidity_input)
        serverroom_humidity_level['high'] = fuzz.interp_membership(self.serverroom_humidity['range'], self.serverroom_humidity['high'], serverroom_humidity_input)
        serverroom_humidity_level['very_high'] = fuzz.interp_membership(self.serverroom_humidity['range'], self.serverroom_humidity['very_high'], serverroom_humidity_input)
        
        #Rueles
        rule1 = np.fmin(serverroom_temperature_level['hot'], self.cooler['high'])
        rule2 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['warm']), serverroom_humidity_level['very_high']), self.cooler['high'])
        rule3 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['warm']), serverroom_humidity_level['high']), self.cooler['high'])
        rule4 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['warm']), serverroom_humidity_level['normal']), self.cooler['high'])
        rule5 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['warm']), serverroom_humidity_level['low']), self.cooler['medium'])

        rule6 = np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['hot']) , self.cooler['high'])

        rule10 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['warm']), serverroom_humidity_level['low']), self.cooler['medium'])

        rule11 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['warm']), serverroom_humidity_level['very_high']) , self.cooler['high'])
        rule12 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['warm']), serverroom_humidity_level['high']), self.cooler['medium'])
        rule13 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['warm']), serverroom_humidity_level['normal']), self.cooler['medium'])
        rule14 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['warm']), serverroom_humidity_level['low']), self.cooler['low'])

        rule15 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['mild']), serverroom_humidity_level['low']), self.cooler['zero'])
        rule16 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['mild']), serverroom_humidity_level['normal']), self.cooler['low'])
        rule17 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['mild']), serverroom_humidity_level['high']), self.cooler['low'])
        rule18 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['mild']), serverroom_humidity_level['very_high']), self.cooler['medium'])
        rule19 = np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['cold']), self.cooler['zero'])
        rule20 = np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['mild']), self.cooler['zero'])

        rule21 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], 
                                 softwareroom_temperature_level['warm']), 
                         serverroom_humidity_level['very_high']), 
                self.cooler['low'])

        rule22 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['hot']), serverroom_humidity_level['very_high']), self.cooler['low'])

        rule23 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['warm']), serverroom_humidity_level['high']), self.cooler['zero'])
        rule24 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['warm']), serverroom_humidity_level['normal']), self.cooler['zero'])
        rule25 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['warm']), serverroom_humidity_level['low']), self.cooler['zero'])

        rule26 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['hot']), serverroom_humidity_level['high']), self.cooler['zero'])
        rule27 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['hot']), serverroom_humidity_level['normal']), self.cooler['zero'])
        rule28 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['hot']), serverroom_humidity_level['low']), self.cooler['zero'])

        #new rules 
        rule29 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['cold']), serverroom_humidity_level['very_high']), self.cooler['zero'])
        rule30 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['cold']), serverroom_humidity_level['high']), self.cooler['zero'])
        rule31 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['warm']), serverroom_humidity_level['very_high']), self.cooler['low'])
        rule32 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['cold']), serverroom_humidity_level['normal']), self.cooler['zero'])
        rule33 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['mild']), serverroom_humidity_level['very_high']), self.cooler['zero'])
        rule34 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['cold'], softwareroom_temperature_level['cold']), serverroom_humidity_level['normal']), self.cooler['zero'])
        rule35 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['cold']), serverroom_humidity_level['very_high']), self.cooler['medium'])
        rule36 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['mild']), serverroom_humidity_level['high']), self.cooler['medium'])
        rule37 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['mild']), serverroom_humidity_level['normal']), self.cooler['medium'])
        rule38 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['hot']), serverroom_humidity_level['normal']), self.cooler['medium'])
        rule39 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['hot']), serverroom_humidity_level['high']), self.cooler['medium'])
        rule40 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['cold']), serverroom_humidity_level['very_high']), self.cooler['low'])
        rule41 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['mild'], softwareroom_temperature_level['cold']), serverroom_humidity_level['high']), self.cooler['zero'])
        rule42 = np.fmin(np.fmin(np.fmin(serverroom_temperature_level['warm'], softwareroom_temperature_level['mild']), serverroom_humidity_level['low']), self.cooler['medium'])
       
        serverroom_temp_in_category = False
        softwareroom_temp_in_category = False
        serverroom_humidity_in_category = False

        # for key in serverroom_temperature_level:
        #     if serverroom_temperature_level[key] > 0:
        #         print(f"Server Room Temp: {serverroom_temperature_input} is in '{key}' category")
        #         serverroom_temp_in_category = True

        # if not serverroom_temp_in_category:
        #     print(f"Server Room Temp: {serverroom_temperature_input} does not lie in any category.")

        # for key in softwareroom_temperature_level:
        #     if softwareroom_temperature_level[key] > 0:
        #         print(f"Software Room Temp: {softwareroom_temperature_input} is in '{key}' category")
        #         softwareroom_temp_in_category = True

        # if not softwareroom_temp_in_category:
        #     print(f"Software Room Temp: {softwareroom_temperature_input} does not lie in any category.")

        # # Checking server room humidity
        # for key in serverroom_humidity_level:
        #     if serverroom_humidity_level[key] > 0:
        #         print(f"Server Room Humidity: {serverroom_humidity_input} is in '{key}' category")
        #         serverroom_humidity_in_category = True

        # # If no category matches
        # if not serverroom_humidity_in_category:
        #     print(f"Server Room Humidity: {serverroom_humidity_input} does not lie in any category.")


        print("")

    
        cooler_activation = {}


        cooler_activation['zero'] = np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin(np.fmin
                                                                                    (np.fmin(np.fmin(rule28, 
                                                                                    rule27), 
                                                                                    rule26), rule20), rule19), 
                                                                                    rule15),rule23), rule24), rule25, rule29), 
                                                                                    rule30), rule32), rule33), rule34), rule41)
         
        cooler_activation['low'] = np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(rule14, rule16), rule17), rule21), rule22), rule31), rule40)
        cooler_activation['medium'] = np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(rule10, rule12), 
                                                              rule13), rule5), rule18), rule35), 
                                                              rule36), rule37), rule38), rule39), rule42)
        
        cooler_activation['high'] = np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(rule1, 
                                                                                    rule2), rule2), rule3), 
                                                                                    rule4), rule11), 
                                                                                    rule6)
        

        aggregated = np.fmax(np.fmax(np.fmax(cooler_activation['zero'], cooler_activation['low']), 
                                    cooler_activation['medium']), cooler_activation['high'])
        # print('aggregated', aggregated)
        # print(f"Server Room Temp Memberships: {serverroom_temperature_level}")
        # print(f"Software Room Temp Memberships: {softwareroom_temperature_level}")
        # print(f"Server Room Humidity Memberships: {serverroom_humidity_level}")


        if np.all(aggregated == 0):
            defuzzified =  0
        else:
            defuzzified  = fuzz.defuzz(self.cooler['range'], aggregated, 'centroid')
        return defuzzified


serverroom_temp_range = Config['fuzzy']['range']['serverroom_temperature']
softwareroom_temp_range = Config['fuzzy']['range']['softwareroom_temperature']
serverroom_humidity_range = Config['fuzzy']['range']['serverroom_humidity']

for _ in range(5):
    fuzzy = Cooler_fan_fuzzy()
    serverroom_temperature = np.random.randint(serverroom_temp_range[0], serverroom_temp_range[-1])
    softwareroom_temperature = np.random.randint(softwareroom_temp_range[0], softwareroom_temp_range[-1])
    serverroom_humidity = np.random.randint(serverroom_humidity_range[0], serverroom_humidity_range[-1])
    
    print(f"Server Room Temp: {serverroom_temperature}, Software Room Temp: {softwareroom_temperature}, Server Room Humidity: {serverroom_humidity}")
    print(fuzzy.compute_fan_speed(serverroom_temperature, softwareroom_temperature, serverroom_humidity))
