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
    ATTRIBUTE_DRIVERNAME = AttributeSchema("drivername",str, True, "DriverName") 
    ATTRIBUTE_AVAILABLE = AttributeSchema("available",bool,True,"If available to pick up a passenger")

	def __init__(self):
		super().__init__("driver_datamodel",[self.ATTRIBUTE_AREA,
									  	 			 self.ATTRIBUTE_ID, self.ATTRIBUTE_AVAILABLE],
									  	 			 "Agent is available to pick up a passenger.")
                                                     
