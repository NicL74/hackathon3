import oef
from oef.agents import OEFAgent

import os, sys
import json
import time

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address, Identity

from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

import agent_dataModel
from agent_dataModel import TIME_AGENT, DRIVER_AGENT, PASSENGER_TRIP

import random
import json
import datetime
import copy

import asyncio

import uuid
import time

#import mlrose
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
from uber_funcs import roads, satnav, calc_distances
from uber_data import block_map_array, manhattan, locations, passengers


class Driver_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        # generate_schema(model_name: str, attribute_values: Dict[str, ATTRIBUTE_TYPES]) -> DataModel:
        # generate_schema('driver_agent',DRIVER_AGENT)      
        
        # Driver's personal parameters (for local storage)
        self.driver_params={}
        self.driver_params['current_block_location'] = 502
        self.driver_params['spare_seats_in_car'] = 4
        self.driver_params['driver_name'] = "Zelda"
        self.earnings_for_day = 0
        self.driver_params['target_earnings_for_day'] = 150
        self.driver_params['target_earnings_per_unit_time'] = 20
        self.driver_params['min_earnings_per_unit_time'] = 10
        self.driver_params['cost_per_unit_distance'] = 0.5
        self.driver_params['actual_earnings_per_unit_time'] = 12
        self.driver_params['speed'] = 30
        
        # Driver's personal parameters (for OEF)
        self.scheme = {}
        self.scheme['area'] = None
        self.scheme['id'] = None
        self.scheme['drivername'] = "Nic"
        self.scheme['available'] = None  
        
        # Driver's store of active quotes
        self.myquotes = {}
        

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
    
        """Acknowledge CFP received"""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))
        
        trip_data={}
        trip_data[origin] = json.loads(query.decode("UTF-8"))
        print(trip_data[origin])
        
        #map_array = block_map_array
        map_array = manhattan
        
        print(locations)
        
        """Driver needs to understand what route is being requested and decide whether to bid or not."""
        passenger_id = trip_data[origin]['passenger_id']
        passenger_name = trip_data[origin]['passenger_name']
        # Locations supplied in format: map block number
        pickup_location = trip_data[origin]['pickup'] 
        destination_location = trip_data[origin]['destination']
        print(pickup_location, destination_location)
        
        print('Driver has received query for trip from '+pickup_location+' to '+destination_location)
        
        """How long is the route being requested? What would be my incurred cost to deliver?"""
        # How can I find this number from the OEF?
        number_of_competitors = np.random.randint(10,60)
        
        cost_of_bid = 0.5 #fet_tx_fee
        
        y,x = np.shape(map_array)
        print(y,x)
        
        # I need to convert a location name to a block number
        num_locations = np.shape(locations)[0]
        for row in range(0,num_locations):
            if(locations[row][0]==pickup_location):
                xp = int(locations[row][1])
                yp = int(locations[row][2])
            if(locations[row][0]==destination_location):
                xd = int(locations[row][1])
                yd = int(locations[row][2])
        print(xp,yp,xd,yd)
        
        # Run a check on the block values at these locations to ensure they are not blank
        pickup_block_val = map_array[yp-1,xp-1]
        print('Pickup block val = '+str(pickup_block_val))
        destination_block_val = map_array[yd-1,xd-1]
        print('Destination block val = '+str(destination_block_val))
            
        # Convert from x and y in blocks into a block number (starting at 1 and zig-zagging left to right, top to bottom)
        pickup_block = xp + x*(yp-1)
        destination_block = xd + x*(yd-1)
        print('pickup location: '+pickup_location+' (Block: '+str(pickup_block)+')')
        print('Destination location: '+destination_location+' (Block: '+str(destination_block)+')')
        
        # Use the 'satnav' function to calculate a route and a distance for requested route
        (route_vector, distance, instructions, roadmap) = satnav(map_array,pickup_block,destination_block,0) #display_on = 0
        distance1 = distance
        print('Distance of requested route = '+str(distance1))
        speed = self.driver_params['speed']
        time1 = distance1/speed
        cost_per_unit_distance = self.driver_params['cost_per_unit_distance']
        cost1 = cost_per_unit_distance * distance1
        # Use the 'satnav' function to calculate a route and a distance from current location to pickup point 
        current_location = self.driver_params['current_block_location']
        print('current location: '+str(current_location))
        if(current_location==pickup_block):
            distance2 = 0
        else:
            (route_vector, distance, instructions, roadmap) = satnav(map_array,current_location,pickup_block,0)
            distance2 = distance
        print('Distance from current location to pickup point = '+str(distance2))
        time2 = distance2/speed
        cost2 = cost_per_unit_distance * distance2
        # Calculate total cost and time to deliver the job would be 
        total_cost = cost1 + cost2
        print('Total cost to deliver job: '+str(total_cost)+' (based on cost per distance of '+str(cost_per_unit_distance)+')')
        total_time = time1 + time2
        print('Total time to deliver job: '+str(total_time))
        target_earnings_per_unit_time = self.driver_params['target_earnings_per_unit_time']
        print('Target earnings per unit time: '+str(target_earnings_per_unit_time))
        # Calculate a target price for job (to deliver target earnings_per_unit time) and minimum price
        target_price = total_cost + target_earnings_per_unit_time*total_time
        print('Target price for job: '+str(target_price))
        min_earnings_per_unit_time = self.driver_params['min_earnings_per_unit_time']        
        min_price = total_cost + min_earnings_per_unit_time*total_time
        # Calculate likelihood of successful bid
        num_bidders = number_of_competitors+1 #'''Would need to get this number from OEF'''
        print('Number of bidders: '+str(num_bidders))
        '''Ideally I would include some weighting to take into account how close to pickup I am'''
        successful_bid_likelihood = (1/(distance2+1.1))**(num_bidders-1)**.05
        print('Successful bid likelihood: '+str(successful_bid_likelihood))
        # Calculate profit if bid accepted
        potential_profit = target_earnings_per_unit_time*total_time
        print('Potential profit: '+str(potential_profit))
        # Calculate expected profit, taking into account likelihood of successful bid
        expected_profit = potential_profit * successful_bid_likelihood
        print('Expected_profit = '+str(expected_profit))
        print('Cost of bid = '+str(cost_of_bid))
        # Compare expected profit vs. cost of bidding, to decide whether or not to bid (binary val)
        worth_bidding = expected_profit>cost_of_bid
        bid_price = int(target_price) # for some reason a float64 doesn't work
        
        # If worth_bidding is true, set the bid_price to the target_price
        if(worth_bidding):
            
            """If driver decides to bid, send a simple Propose to the sender of the CFP."""                    
            #format the price for number extraction on other agent
            proposal = Description({"price" : bid_price})
            print("[{0}]: Sending propose at price: {1}".format(self.public_key, bid_price))
            self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
            startBalance = api.tokens.balance(server_agentID)
            # Keep track of quotes
            self.myquotes[origin]={
                "pickup": trip_data[origin]['pickup'],
                "destination": trip_data[origin]['destination'],
                "bid_price": bid_price
            }
            
        # If worth_bidding is false, decline to bid
        else:
            print("[{0}]: Declining to bid, at expected profit: {1} vs. cost of bid: {2}".format(self.public_key, expected_profit, cost_of_bid))
            self.send_decline(msg_id + 1, dialogue_id, origin, target + 1)
            
    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):

        """Once we received an Accept, check the correct funds have been received. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))
        
        # Get the passenger name from the original CFP? Hard code for now
        passenger_name = "Angela"
        driver_name = self.driver_params['driver_name']
        pickup_location = self.myquotes[origin]['pickup']

        if startBalance < api.tokens.balance(server_agentID):
            command = {}
            #command["time"] = int(time.time())
            command["message"] = ("All set {0}! Your driver, {1}, will pick you up at: {2}".format(passenger_name, driver_name, pickup_location))
            msg = json.dumps(command)
            self.send_message(0,dialogue_id, origin, msg.encode())

            print('Final Balance: ', api.tokens.balance(server_agentID))
            quoted_bid = self.myquotes[origin]['bid_price']
            print('quoted_bid = '+str(quoted_bid))
            self.myquotes[origin] = {} # Clear the entry
            self.earnings_for_day += quoted_bid  
            # Check if driver has earned enough for the day?
            earnings_progress = self.earnings_for_day/self.driver_params['target_earnings_for_day']
            if(earnings_progress >= 1):
                print("{0} % of target earnings achieved, so I'm off home!".format("%.2f" % (earnings_progress*100)))
                server_agent.scheme['available'] = False
                # Update the service on the OEF
                server_agent.description = Description(server_agent.scheme, DRIVER_AGENT())
                server_agent.register_service(0,server_agent.description)
            else:
                print("{0} % of target earnings achieved, so got to keep going!".format("%.2f" % (earnings_progress*100)))
                
        else:
            print('No Funds Sent!')
            print('Ending Dialogue')
            return


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")
        self.myquotes[origin] = {}
        '''May decide to make improved bid to'''


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #locate the agent account entity for interacting with the ledger.
    with open ('./workdir/UberX/server_private.key', 'r') as private_key_file:
        server_agentID = Entity.load(private_key_file)

    startBalance = api.tokens.balance(server_agentID)
    print('startBalance = '+str(startBalance))

    #set trading values
    price = 200 #bid_price # Need to set this to appropriate value for each bid, based on various parameters
    fet_tx_fee = 40

    print('Price:', price)
    print('Balance Before:', startBalance)

    # create agent and connect it to OEF
    server_agent = Driver_Agent(str(Address(server_agentID)), oef_addr="127.0.0.1", oef_port=10000)
    server_agent.scheme['area'] = 3
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.scheme['drivername'] = "Nic"
    server_agent.scheme['available'] = True
    server_agent.connect()
    
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, DRIVER_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()
