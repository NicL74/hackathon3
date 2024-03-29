
from typing import List

import oef
from oef.agents import OEFAgent
from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address, Identity

import agent_dataModel
from agent_dataModel import TIME_AGENT, DRIVER_AGENT, PASSENGER_TRIP

import json
import datetime

import sys
import time
import uuid
import asyncio

#import mlrose
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
from uber_funcs import roads, satnav, calc_distances
from uber_data import block_map_array, manhattan, locations, passengers


class ClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """
    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0
        self.block_location = 496
        num_locations,x = np.shape(locations)
        self.num_locations = num_locations
        self.passenger_name = "Angela"


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("Received message: origin={}, dialogue_id={}, content={}".format(origin, dialogue_id, content))
        data = json.loads(content.decode())
        print ("message...")
        print(data)
        print('Final Balance:', api.tokens.balance(client_agentID))
        time.sleep(10)
        self.stop()

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))
        
        # How do we construct the cfp? 
        # This is where we define pickup and destination locations (and whether UberX or UberPool later)
        
        #print(locations[0][0])
        #print(locations[2][0])
        p = np.random.randint(0,self.num_locations)
        d = np.random.randint(0,self.num_locations)
        if(p==d):
            if(p>0):
                p -= 1
            else:
                p += 1
        pickup_location = locations[p][0]
        destination_location = locations[d][0]
        
        #trip_query = Query([Constraint("pickup_location_name", Eq(str(locations[0][0]))), Constraint("destination_location_name", Eq(str(locations[2][0])))],PASSENGER_TRIP())
        trip_query = json.dumps({"pickup": pickup_location, \
        "destination": destination_location, \
        "passenger_id": 42, \
        "passenger_name": self.passenger_name}) .encode("UTF-8")
        
        # Pick a couple of predefined locations for my query pickup and destination (ideally make it rand pick)
        #my_query["pickup_location_name"] = uber_data.locations[0][0]
        #my_query["destination_location_name"] = uber_data.locations[2][0]
        

        for agent in agents:

            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            self.pending_cfp += 1            
            self.send_cfp(1, 0, agent, 0, trip_query)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, check if we can afford the data. If so we accept, else we decline the proposal."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))

        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})

        received_cfp = len(self.received_proposals) + self.received_declines

        #sort the multiple proposals by price
        self.received_proposals.sort(key = lambda i: (i['proposal']['price']))

        # once everyone has responded, let's accept them.
        if received_cfp == self.pending_cfp :
            print("I am here")
            if len( self.received_proposals) >= 1 :
                proposed = str(self.received_proposals[0]['proposal'])
                price = [int(s) for s in proposed.split() if s.isdigit()]
                #check if we can afford the data.
                if api.tokens.balance(client_agentID) > self.received_proposals[0]['proposal']['price'] :
                    #if we can, transfer tokens from the client account to the proposal address.
                    api.sync(api.tokens.transfer(client_agentID, Address(self.received_proposals[0]['agent']) , self.received_proposals[0]['proposal']['price'], 20))
                    self.send_accept(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                    print ("Accept")
                else :
                    print("Not enough tokens!")
                    #cannot afford! Decline the proposal.
                    self.send_decline(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                    self.stop()
            else :
                print("They don't have data")
                self.stop()

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("Received a decline!")
        self.received_declines += 1
        self.stop()

if __name__ == '__main__':

    #define the ledger parameters
    api = LedgerApi('127.0.0.1', 8100)

    #locate the client account entity for interacting with the ledger.
    with open ('./workdir/UberX/client_private.key', 'r') as private_key_file:
        client_agentID = Entity.load(private_key_file)

    # define an OEF Agent
    client_agent = ClientAgent(str(Address(client_agentID)), oef_addr="127.0.0.1", oef_port=10000)

    print('Balance Before:', api.tokens.balance(client_agentID))

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers (i.e. available drivers in the area)
    my_current_area = 3 # Ideally we would keep track of this and update accordingly
    echo_query1 = Query([Constraint("area", Eq(my_current_area)), Constraint("available", Eq(True))],DRIVER_AGENT())
    client_agent.search_services(0, echo_query1)
    client_agent.run()
