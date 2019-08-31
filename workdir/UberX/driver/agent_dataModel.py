from typing import List
import os, sys

from oef.query import Eq, Range, Constraint, Query, AttributeSchema
from oef.schema import DataModel, Description , Location


class TIME_AGENT (DataModel):
	ATTRIBUTE_TIMEZONE = AttributeSchema("timezone", int, True, "TimeZone")
	ATTRIBUTE_ID = AttributeSchema("id", str, True, "Id")
	ATTRIBUTE_TWENTYFOUR = AttributeSchema("twentyfour", bool, False, "If the clock is twentyfour hour" )


	def __init__(self):
		super().__init__("time_datamodel",[self.ATTRIBUTE_TIMEZONE,
									  	 			 self.ATTRIBUTE_ID, self.ATTRIBUTE_TWENTYFOUR],
									  	 			 "Agent has the time.")

class DRIVER_AGENT (DataModel):
	ATTRIBUTE_AREA = AttributeSchema("area", int, True, "Area")
	ATTRIBUTE_ID = AttributeSchema("id", str, True, "Id")
	ATTRIBUTE_DRIVERNAME = AttributeSchema("drivername", str, True, "DriverName") 
	ATTRIBUTE_AVAILABLE = AttributeSchema("available", bool, True, "If available to pick up a passenger")
    

	def __init__(self):
		super().__init__("driver_datamodel",[self.ATTRIBUTE_AREA,
									  	 			 self.ATTRIBUTE_ID, self.ATTRIBUTE_DRIVERNAME, self.ATTRIBUTE_AVAILABLE],
									  	 			 "Driver is potentially available to pick up a passenger.")

class PASSENGER_TRIP (DataModel):
    ATTRIBUTE_PICKUP = AttributeSchema("pickup_location_name", str, True, "Pickup location name")
    ATTRIBUTE_ID = AttributeSchema("id", str, True, "Id")
    ATTRIBUTE_DESTINATION = AttributeSchema("destination_location_name", str, True, "Destination location name")

    def __init__(self):
        super().__init__("trip_datamodel",[self.ATTRIBUTE_PICKUP,
									  	 			 self.ATTRIBUTE_ID, self.ATTRIBUTE_DESTINATION],
									  	 			 "Passenger trip is defined.")
