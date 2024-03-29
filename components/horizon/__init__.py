import os, sys
sys.path.append('../../')
import json
import asyncio
import pytz
from helpers.logger import formatLogger
from astral import *
from time import strftime, strptime
from datetime import datetime, timedelta, tzinfo
from helpers.db import *
from helpers.dt import *

logger = formatLogger(__name__)

# DATE_STR_FORMAT = "%Y-%m-%d"
# UTC = DEFAULT_TIME_ZONE = pytz.utc
# ZERO = timedelta(0)

def sun_horizon(sunrise,sunset): #if 1 above horizon if 0 below horzion
	now_utc = datetime.now()
	horizon = False 
	if(now_utc > sunrise and now_utc < sunset):
		horizon = True	
	return horizon
			

def local_astral_event():
	a = Astral()
	latitude = float(getParmeters("horizon","lat"))
	longitude = float(getParmeters("horizon","lon"))
	location = Location(info = (getParmeters("horizon","city"), getParmeters("horizon","state"), latitude, longitude, getParmeters("horizon","timezone"), 100))
	a.solar_depression = "civil"
	timezone = getParmeters("horizon","timezone")
	#location.timezone = config_data["timezone"]
	sun = location.sun(date=datetime.today(), local=True)
	data = {}
	data["sunrise"] = sun["sunrise"]
	data["sunset"] = sun["sunset"]
	data["timezone"] = timezone
	return data


async def horizonHandler():
	while True:
		astral = local_astral_event()
		time_now = datetime.now()
		sun_horizon_position = sun_horizon(utc_aware_to_datetime(astral["sunrise"]), utc_aware_to_datetime(astral["sunset"]))
		data = {}
		data["location"] = {}
		data["astral"] = {}
		data["astral"]["next_time"] = {}
		data["location"]["city"] = getParmeters("horizon","city")		
		data["location"]["state"] = getParmeters("horizon","state")			
		data["location"]["latitude"] = getParmeters("horizon","lat")			
		data["location"]["longitude"] = getParmeters("horizon","lon")	
		data["location"]["timezone"] = str(astral["timezone"])
		data["astral"]["sunrise"] = str(utc_aware_to_datetime(astral["sunrise"]))
		data["astral"]["sunset"] = str(utc_aware_to_datetime(astral["sunset"]))
		data["astral"]["above_horizon"] = str(sun_horizon_position).lower()
		if(sun_horizon_position):
			data["astral"]["next_astral"] = "sunset"
			data["astral"]["next_time"] = get_age(utc_aware_to_datetime(astral["sunset"]))
		else:
			data["astral"]["next_astral"] = "sunrise"	
			if(time_now > utc_aware_to_datetime(astral["sunset"])):
				tommorrow = utc_aware_to_datetime(astral["sunrise"]) + timedelta(days=1)
				data["astral"]["next_time"] =  get_age(tommorrow)
			else:
				data["astral"]["next_time"] =  get_age(utc_aware_to_datetime(astral["sunrise"]))
		deviceActions = {}
		deviceProperties = data
		dbStore("components",{"id":"horizon","actions":deviceActions,"properties":deviceProperties})
		logger.info("%s" % str(deviceProperties))
		await asyncio.sleep(60)


class  horizon(object):
	def __init__(self):
		pass
        
	def validateProperties(self,getDevice,conditionProperties,conditionType):
		validStatus = False
		getDeviceProperties = getDevice["properties"]
		getDevicePropertiesKeys = []
		for key, value in getDeviceProperties.items():
			getDevicePropertiesKeys.append(key)    
		for key, value in conditionProperties.items():
			if key in getDevicePropertiesKeys:
				if isinstance(value,dict):
					for k, v in value.items():
						getDeviceProperty= getDeviceProperties[key][k]
						getIfProperty = conditionProperties[key][k]
				else:
					getDeviceProperty = getDeviceProperties[key]
					getIfProperty = conditionProperties[key]
					
				if conditionType == "=":
					if getDeviceProperty == getIfProperty:
						validStatus = True
		return validStatus
