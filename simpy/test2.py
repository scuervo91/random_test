import simpy
import numpy as np

class FlowStation:
    def __init__(self,env,num_chargers,tanks_capacity,max_level, trucks_num):
        self.env = env
        self.dispenser = simpy.Resource(env,capacity= num_chargers)
        self.tanks = simpy.Container(env,init=100,capacity=tanks_capacity)
        self.max_level = max_level
        self.monitor_tank = env.process(self.monitor_tank(env,max_level))
        self.trucks = simpy.Resource(env,capacity=trucks_num)
        
    def monitor_tank(self, env, max_level):
        while True:
            print(f'The tank has {self.tanks.level} bbl at {env.now}')
            if self.tanks.level >= max_level:
                print(f'Calling Trucks at {env.now}')
                env.process(charge_trucks(env,self))
                env.process(charge_trucks(env,self))
            yield env.timeout(1)
            
trucks = simpy.Resource


def charge_trucks(env,flow_station):
    with flow_station.trucks.request() as truck_req:
        #Trucks delays 2 days to arrive
        yield truck_req
        yield env.timeout(2)
        print(f'Truck has arrived at {env.now}')
        with flow_station.dispenser.request() as req:
            yield req
            print(f'Trucks started to load oil at {env.now}')
            level_before = flow_station.tanks.level
            yield flow_station.tanks.get(250)
            level_after = flow_station.tanks.level
            yield env.timeout(0.2)
            print(f'Trucks ended to load oil at {env.now}')
            print(f' Inital level: {level_before}\n final level {level_after}')
            


def well(name,env,flow_station,rate):
    while True:
        yield env.timeout(1)
        if flow_station.tanks.level < flow_station.max_level:
            print(f'Well {name} producing at a {rate} bbl/d {env.now}')
            yield flow_station.tanks.put(rate)
            
        else:
            print(f'Well {name} not produced at {env.now}')
            
        

def well_generator(env,flow_station, wells_num):
    rates = np.random.uniform(low=100, high=200, size=wells_num)
    for i,r in enumerate(rates):
        env.process(well(i,env,flow_station,r))
    yield env.timeout(1)
        
env = simpy.Environment()
flow_station = FlowStation(env,2,8000,6000,5)
well_gen = env.process(well_generator(env,flow_station,4))
env.run(until=40)
        
        
    
    