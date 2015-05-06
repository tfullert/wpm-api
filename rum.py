# =============================================================================
# rum.py
#
# A class to help facilitate API calls to the 'rum' service for WPM.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 12/06/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class RUM(Client):

	# -------------------------------------------------------------------------
	# Create a new RUM object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'rum', '', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of RUM object.
	def __str__(self):
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# API interaction to create a beacon.
	# 
	# params - Dictionary containing details of beacon.
	#  * beaconName: Name of the beacon to create.
	def createBeacon(self, params):
		self.setService('rum')
		self.setMethod('beacon')
		self.setHttpMethod('POST')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to list beacons.
	def listBeacons(self):
		self.setService('rum')
		self.setMethod('beacon')
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to update a beacon.
	def updateBeacon(self, beaconId, params):
		self.setService('rum')
		self.setMethod('beacon/' + beaconId)
		self.setHttpMethod('PUT')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to delete a beacon.
	def deleteBeacon(self, beaconId):
		self.setService('rum')
		self.setMethod('beacon/' + beaconId)
		self.setHttpMethod('DELETE')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get performance summary on recent data.
	# 
	# params - Dictionary of parameters
	#  * beaconId: ID of the beacon to get summary for.
	#  * minutes: Number of minutes (between 1 and 60) to aggregate on.
	#  * allbeacons: Flag to get summary for all beacons (1) or just one (0).
	def getPerformanceSummaryOnRecentData(self, params):
		self.setService('rum')
		self.setMethod('data/summary')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get recent time series data.
	# 
	# params - Dictionary of parameters
	#  * beaconId: The ID of the beacon to get data for.
	#  * minutes: Number of minutes (between 1 and 60) to get data for.
	def getRecentTimeSeriesData(self, params):
		self.setService('rum')
		self.setMethod('data/ts/recent')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get time series data for a beacon.
	#
	# params - Dictionary of parameters.
	#  * beaconId: ID of beacon to get data for.
	#  * startDate: Start date to get data for.
	#  * endDate: End date to get data form.
	#  * type: Day level (daily) or minute level data.
	def getTimeSeriesData(self, params):
		self.setService('rum')
		self.setMethod('data/ts')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get raw data for a beacon.
	#
	# params - Dictionary of parameters.
	#  * beaconId: The ID of the beacon to get data for.
	#  * startDate: The start date to get data for (ISO 8601 formatted datetime).
	#  * endDate: The end date to get data for (ISO 8601 formatted datetime).
	#  * offset: The position to start from.
	#  * limit: The number of samples to get data for.
	#  * orderbypageloadtime: ('asc' or 'desc') to order data by page load time.
	#  * errorsonly: Set to 1 if only samples with JavaScript errors should be returned.
	#  * urlexact: Filter samples by the exact url.
	#  * url: Filter samples by url using a regular expression.
	#  * browser: Filter samples by browser type.
	#  * connection_type: Filter samples by connection type.
	#  * country: Filter samples by country.
	#  * jserr: Filter samples by JS error filename or string (regex).
	def getRawData(self, params):
		self.setService('rum')
		self.setMethod('data/raw')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get analysis data.
	#
	# params - Dictionary of parameters.
	#  * beaconId: The ID of the beacon to get data for.
	#  * startDate: The start date to get data for (ISO 8601 formatted datetime).
	#  * endDate: The end date to get data for (ISO 8601 formatted datetime).
	#  * groupby: Key to group data by. This parameter is required if 'overtime' is not set to 1.
	#  * overtime: Set to 1 if you want results to be returned over time. 
	#    If this flag is not set to 1 the 'groupby' field becomes required. 
	#    Note that this parameter is ignored when grouping by JS error.
	#  * url: Filter samples by url using a regular expression.
	#  * browser: Filter samples by browser type.
	#  * connection_type: Filter samples by connection type.
	#  * country: Filter samples by country.
	#  * jserr: Filter samples by JS error filename or string (regex).
	def getAnalysisData(self, params):
		self.setService('rum')
		self.setMethod('data/analysis')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get object level time series data for a beacon.
	#
	# params - Dictionary of parameters.
	#  * beaconId: The ID of the beacon to get data for.
	#  * startDate: The start date to get data for (ISO 8601 formatted datetime).
	#  * endDate: The end date to get data for (ISO 8601 formatted datetime).
	def getObjectLevelTimeSeriesData(self, params):
		self.setService('rum')
		self.setMethod('data/ol/ts')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get object level outlier data for a beacon.
	#
	# params - Dictionary of parameters.
	#  * beaconId: The ID of the beacon to get data for.
	#  * startDate: The start date to get data for (ISO 8601 formatted datetime).
	#  * endDate: The end date to get data for (ISO 8601 formatted datetime).
	#  * groupby: Key to group the data by (resource, domain, location_resource, location_domain).	
	def getObjectLevelOutliersData(self, params):
		self.setService('rum')
		self.setMethod('data/ol/outlier')
		self.setHttpMethod('GET')
		return self.call(params)

# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import json
	import time
	import string
	import random
	from tester import Tester
	from datetime import datetime, timedelta

	# Variables for testing	
	key		= Tester.wpmAPIKey
	secret	= Tester.wpmAPISecret

	# Create a random service name
	beaconName	= ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))

	# Dates for getting raw data
	startDate	= (datetime.now() - timedelta(minutes=300)).strftime("%Y-%m-%dT%H:%M:%S")
	endDate		= datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	print 'Setting Start Date: ' + startDate
	print 'Setting End Date: ' + endDate

	# TODO: This beacon ID is for testing the API calls that get sample data.  
	# If you use the beacon that is created as part of the other tests you'll have to
	# include a rather long sleep (for a 1 minute monitoring a sleep of 4 minutes wasn't
	# sufficient).  I recommend setting up a beacon in your account that is always on for
	# testing purposes.  Then set the testBeacon value to the beacon ID for that beacon.
	testBeacon = ''

	# Test beacon name
	rumParams = { 'beaconName' : 'APITEST_' + beaconName } 

	# Test __init__
	print '**** TEST: __init__'
	rumClient = RUM(key, secret)
	print rumClient

	# Test __str__
	print '**** TEST: __str__'
	print rumClient

	# Test createBeacon
	print '**** TEST: createBeacon'
	response	= rumClient.createBeacon(rumParams)
	jsonObj		= json.loads(response.text)
	beaconId	= jsonObj.get('data', {}).get('items', {}).get('beaconId', '')
	print 'Got BeaconId: ' + beaconId

	# Test listBeacons
	print '**** TEST: listBeacon'
	response	= rumClient.listBeacons()
	jsonObj		= json.loads(response.text)
	beacons		= jsonObj.get('data', {}).get('items', [])

	for beacon in beacons:
		print 'Beacon: ' + beacon['preferences']['beaconName']

	# Test getPerformanceSummaryOnRecentData
	print '**** TEST: getPerformanceSummaryOnRecentData'	
	rumParams.clear()
	rumParams	= {
		'beaconId'		: '',
		'minutes'		: 60,
		'allbeacons'	: 1,
	}

	beacons		= []
	response	= rumClient.getPerformanceSummaryOnRecentData(rumParams)
	jsonObj		= json.loads(response.text)
	beacons		= jsonObj.get('data', {}).get('items', [])

	for beacon in beacons:
		print 'Beacon: ' + beacon['beaconName']
	
	# Test getRecentTimeSeriesData
	print '**** TEST: getRecentTimeSeriesData'
	rumParams.clear()
	rumParams	= { 'beaconId' : beaconId, 'minutes' : 60 }
	response	= rumClient.getRecentTimeSeriesData(rumParams)
	jsonObj		= json.loads(response.text)	
	print 'TXT: ' + response.text

	# Test getTimeSeriesData
	print '**** TEST: getTimeSeriesData'
	rumParams.clear()
	rumParams	= { 
		'beaconId'	: beaconId,
		'startDate' : startDate,
		'endDate'	: endDate,
		'type'		: '' 
	}
	response	= rumClient.getTimeSeriesData(rumParams)
	print 'TXT: ' + response.text

	# Test getRawData
	print '**** TEST: getRawData'
	rumParams.clear()
	rumParams	= { 'startDate' : startDate, 'endDate' : endDate }	
	response	= rumClient.getRawData(rumParams)	
	print 'TXT: ' + response.text

	# Test getAnalysisData
	print '**** TEST: getAnalysisData'
	rumParams['groupby'] = 'url'
	response	= rumClient.getAnalysisData(rumParams)
	print 'TXT: ' + response.text

	# Test getObjectLevelTimeSeriesData
	print '**** TEST: getObjectLevelTimeSeriesData'
	rumParams.clear()
	rumParams	= { 'beaconId' : beaconId, 'startDate' : startDate, 'endDate' : endDate }
	response	= rumClient.getObjectLevelTimeSeriesData(rumParams)
	print 'TXT: ' + response.text

	# Test getObjectLevelOutliersData
	print '**** TEST: getObjectLevelOutlierData'
	rumParams['groupby'] = 'resource'
	response 	= rumClient.getObjectLevelOutliersData(rumParams)
	print 'TXT: ' + response.text

	# Test updateBeacon
	print '**** TEST: updateBeacon'
	rumParams.clear()
	rumParams	= { 'beaconName' : beaconName + '_UPDATED' }
	response	= rumClient.updateBeacon(beaconId, rumParams)
	jsonObj		= json.loads(response.text)

	# Test deleteBeacon
	print '**** TEST: deleteBeacon'
	time.sleep(5)
	response	= rumClient.deleteBeacon(beaconId)
	print 'TXT: ' + response.text
