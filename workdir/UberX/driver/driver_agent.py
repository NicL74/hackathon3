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
from uber_data import block_map_array, locations, passengers


class Driver_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        # generate_schema(model_name: str, attribute_values: Dict[str, ATTRIBUTE_TYPES]) -> DataModel:
        # generate_schema('driver_agent',DRIVER_AGENT)      
 
        driver_service_description = Description(
            {
                "area": True,
                "id": True,
                "drivername": True,
                "available": True
            },
            DRIVER_AGENT            
        )
        '''
        self.scheme = {}
        self.scheme['area'] = None
        self.scheme['id'] = None
        self.scheme['drivername'] = None
        self.scheme['available'] = None    
        self.scheme['uberx'] = None
        self.scheme['uberpool'] = None
        '''  

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
    
        """Acknowledge CFP received"""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))
        
        """Driver needs to understand what route is being requested and decide whether to bid or not."""
        passenger_id = 2
        passenger_name = "Angela"
        # Locations supplied in format: map block number
        pickup_location = 4 # How do I read parameter values from a CFP?
        destination_location = 8
        
        """How long is the route being requested? What would be my incurred cost to deliver?"""
        # Driver's personal parameters 
        cost_per_unit_distance = 1
        target_earnings_per_unit_time = 0.5
        min_earnings_per_unit_time = 0.2
        target_daily_profit = 100
        profit_today_sofar = 20
        actual_earnings_per_unit_time = 0.3
        speed = 2
        current_location = 5 # Need to keep track of this and update as move
        
        cost_of_bid = 0.5 #fet_tx_fee
        
        
        # Use the 'satnav' function to calculate a route and a distance for requested route
        (route_vector, distance, instructions, roadmap) = satnav(map_array,pickup_location,destination_location,0) #display_on = 0
        distance1 = distance
        print('distance1 = '+str(distance1))
        time1 = distance1/speed
        cost1 = cost_per_unit_distance * distance1
        # Use the 'satnav' function to calculate a route and a distance from current location to pickup point 
        (route_vector, distance, instructions, roadmap) = satnav(map_array,current_location,pickup_location,0) #display_on = 0
        distance2 = distance
        time2 = distance1/speed
        cost2 = cost_per_unit_distance * distance1
        # Calculate total cost and time to deliver the job would be 
        total_cost = cost1 + cost2
        total_time = time1 + time2
        # Calculate a target price for job (to deliver target earnings_per_unit time) and minimum price
        target_price = total_cost + target_earnings_per_unit_time*total_time
        min_price = total_cost + min_earnings_per_unit_time*total_time
        # Calculate likelihood of successful bid
        num_bidders = 6 #'''Would need to get this number from OEF'''
        '''Ideally I would include some weighting to take into account how close to pickup I am'''
        successful_bid_likelihood = 1/num_bidders
        # Calculate profit if bid accepted
        potential_profit = target_earnings_per_unit_time*total_time
        # Calculate expected profit, taking into account likelihood of successful bid
        expected_profit = potential_profit * successful_bid_likelihood
        # Compare expected profit vs. cost of bidding, to decide whether or not to bid (binary val)
        worth_bidding = expected_profit>cost_of_bid
        
        # If worth_bidding is true, set the bid_price to the target_price
        if(worth_bidding):
            bid_price = target_price
            """If driver decides to bid, send a simple Propose to the sender of the CFP."""                    
            #format the price for number extraction on other agent
            proposal = Description({"price" : bid_price})
            print("[{0}]: Sending propose at price: {1}".format(self.public_key, bid_price))
            self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
            startBalance = api.tokens.balance(server_agentID)
        # If worth_bidding is false, decline to bid
        else:
            print("[{0}]: Declining to bid, at expected profit: {1} vs. bid price: {2}".format(self.public_key, expected_profit, bid_price))
            self.send_decline(msg_id + 1, dialogue_id, origin, target + 1)
            
    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):

        """Once we received an Accept, check the correct funds have been received. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        if startBalance < api.tokens.balance(server_agentID):
            command = {}
            #command["time"] = int(time.time())
            command["message"] = ("{0}, your driver,{1}, will pick you up at: {2}".format(passenger_name, driver_name, pickup_location))
            msg = json.dumps(command)
            self.send_message(0,dialogue_id, origin, msg.encode())

            print('Final Balance:', api.tokens.balance(server_agentID))
        else:
            print('No Funds Sent!')
            print('Ending Dialogue')
            return


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")
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
    server_agent.connect()
    
    # register a service on the OEF
    server_agent.register_service(0,server_agent.driver_service_description)
    server_agent.run()
