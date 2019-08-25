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
from agent_dataModel import TIME_AGENT,DRIVER_AGENT

import random
import json
import datetime
import copy

import asyncio

import uuid
import time

class Driver_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        self.scheme = {}
        self.scheme['area'] = None
        self.scheme['id'] = None
        self.scheme['drivername'] = None
        self.scheme['available'] = None    
        self.scheme['uberx'] = None
        self.scheme['uberpool'] = None
        

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Acknowledge CFP received"""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))
        
        """Driver needs to understand what route is being requested and decide whether to bid or not."""
        passenger_id = 
        passenger_name = 
        pickup_location = 
        destination_location = 
        
        """How long is the route being requested? What would be my incurred cost to deliver?"""
        # Driver's personal parameters
        cost_per_unit_distance = 1
        target_earnings_per_unit_time = 0.5
        min_earnings_per_unit_time = 0.2
        target_daily_profit = 100
        profit_today_sofar = 20
        actual_earnings_per_unit_time = 0.3
        
        cost_of_bid = fet_tx_fee
        
        
        # Use the 'satnav' function to calculate a route and a distance for requested route
        distance1 = 12
        speed = 2
        time1 = distance1/speed
        cost1 = cost_per_unit_distance * distance1
        # Use the 'satnav' function to calculate a route and a distance from current location to pickup point 
        distance2 = 12
        speed = 2
        time2 = distance1/speed
        cost2 = cost_per_unit_distance * distance1
        # Calculate total cost and time to deliver the job would be 
        total_cost = cost1 + cost2
        total_time = time1 + time2
        # Calculate a target price for job (to deliver target earnings_per_unit time) and minimum price
        target_price = total_cost + target_earnings_per_unit_time*total_time
        min_price = total_cost + min_earnings_per_unit_time*total_time
        # Calculate likelihood of successful bid
        num_bidders = 6 '''Would need to get this number from OEF'''
        '''Ideally I would include some weighting to take into account how close to pickup I am'''
        successful_bid_likelihood = 1/num_bidders
        # Calculate profit if bid accepted
        potential_profit = target_earnings_per_unit_time*total_time
        # Calculate expected profit, taking into account likelihood of successful bid
        expected_profit = potential_profit * successful_bid_likelihood
        # Compare expected profit vs. cost of bidding, to decide whether or not to bid (binary val)
        worth_bidding = expected_profit>cost_of_bid
        
        
        # Use 'satnav' function to calculate a route from my current position to the pickup point
        cost2 = 0
        distance2 = 3
        
        # Total cost to deliver requested route is sum of two costs
        
        """If driver decides to bid, send a simple Propose to the sender of the CFP."""
        #format the price for number extraction on other agent
        proposal = Description({"price" : price})
        print("[{0}]: Sending propose at price: {1}".format(self.public_key, price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])
        startBalance = api.tokens.balance(server_agentID)

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, check the correct funds have been received. If so send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        if startBalance < api.tokens.balance(server_agentID):
            command = {}
            command["time"] = int(time.time())
            command["message"] = ("{0}, your driver will pick you up at: {1}".format(passenger_name, pickup_location))
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
    with open ('./workdir/Agent2/server_private.key', 'r') as private_key_file:
        server_agentID = Entity.load(private_key_file)

    startBalance = api.tokens.balance(server_agentID)

    #set trading values
    price = journer_price # Need to set this to appropriate value for each bid, based on various parameters
    fet_tx_fee = 40

    print('Price:', price)
    print('Balance Before:', startBalance)

    # create agent and connect it to OEF
    server_agent = Driver_Agent(str(Address(server_agentID)), oef_addr="127.0.0.1", oef_port=10000)
    server_agent.scheme['area'] = 3
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.scheme['drivername'] = "Nic"
    server_agent.scheme['available'] = True
    server_agent.scheme['uberx'] = True
    server_agent.scheme['uberpool'] = True
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, DRIVER_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()
