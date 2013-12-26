# =============================================================================
# maintenanceWindow.py
#
# A class to help facilitate API calls to the 'Maintenance Window' 
# functionality of WPM.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 12/05/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class MaintenanceWindow(Client):

	# -------------------------------------------------------------------------
	# Create a new MaintenanceWindow object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'maintenance', '', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of MaintenanceWindow object.
	def __str__(self):
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# API interaction to create a job for the Instant Test tool.
	#
	# params - Dictionary containing the details of the maintenance window.
	#   * name: Name of the maintenance window.
	# 	* description: Description of the maintenance window.
	#	* recurrence: Should window recur (1, W, M, Y).
	#   * alert: Should monitors alert during window (true/false).
	#   * startDate: Date window should start (ISO 8601 in UTC: 2012-05-10T13:34:00).
	#   * monitor: Array of valid monitor IDs.
	#   * duration: How long (in minutes) the maintenance window will last.
	def createMaintenanceWindow(self, params):
		self.setService('maintenance')
		self.setMethod(self.wpmAPIVersion)
		self.setHttpMethod('POST')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to list all maintenance windows for an account.
	def listMaintenanceWindows(self):
		self.setService('maintenance')
		self.setMethod(self.wpmAPIVersion)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get a specific maintenance window.
	# 
	# maintenanceId - The ID value of the maintenance window to retrieve.
	def getMaintenanceWindow(self, maintenanceId):
		self.setService('maintenance')
		self.setMethod(self.wpmAPIVersion + '/' + maintenanceId)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to create a maintenance window.
	#
	# maintenanceId - ID of the maintenance window to update.
	# params - Dictionary containing the details of the maintenance window.
	#   * name: Name of the maintenance window.
	# 	* description: Description of the maintenance window.
	#	* recurrence: Should window recur (1, W, M, Y).
	#   * alert: Should monitors alert during window (true/false).
	#   * startDate: Date window should start (ISO 8601 in UTC: 2012-05-10T13:34:00).
	#   * monitor: Array of valid monitor IDs.
	#   * duration: How long (in minutes) the maintenance window will last.
	def updateMaintenanceWindow(self, maintenanceId, params):
		self.setService('maintenance')
		self.setMethod(self.wpmAPIVersion + '/' + maintenanceId)
		self.setHttpMethod('PUT')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to delete a maintenance window.
	def deleteMaintenanceWindow(self, maintenanceId):
		self.setService('maintenance')
		self.setMethod(self.wpmAPIVersion + '/' + maintenanceId)
		self.setHttpMethod('DELETE')
		return self.call()
	
# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import json
	from tester import Tester
	from datetime import datetime, timedelta
	
	# Variables for testing	
	key		= Tester.wpmAPIKey
	secret	= Tester.wpmAPISecret

	futureStart	= datetime.now() + timedelta(minutes=900)	
	startDate	= futureStart.strftime("%Y-%m-%dT%H:%M:%S")
	windowName	= 'WINDOW_' + startDate	
	windowDesc	= windowName + ' - Generated via API.'

	mwTestParams = {
		'name'			: windowName,
		'description'	: windowDesc,
		'recurrence'	: '1',
		'alert'			: 'false',
		'startDate'		: startDate,
		'monitor'		: '383b86b85d2411e3a8d89848e167c3b7,3d10693a7abf11e2ae059848e167c3b7',
		'duration'		: '60',
	}

	print 'mwTestParams are:'

	for k, v in sorted(mwTestParams.items()):
		print ' * ', k, '=', v

	# Test __init__
	print '**** TEST: __init__'
	mwClient = MaintenanceWindow(key, secret)
	print mwClient

	# Test __str__
	print '**** TEST: __str__'
	print mwClient

	# Test createMaintenanceWindow
	print '**** TEST: createMaintenanceWindow'
	response	= mwClient.createMaintenanceWindow(mwTestParams)
	jsonObj		= json.loads(response.text)
	windowId	= jsonObj.get('data', {}).get('items', {}).get('id', '')
	print "Created window (ID): " + windowId
	print response.text

	# Test listMaintenanceWindows
	print '**** TEST: listMaintenanceWindows'
	response	= mwClient.listMaintenanceWindows()
	jsonObj		= json.loads(response.text)
	items		= jsonObj.get('data', {}).get('items', {})
	print "Number of maintenance windows: " + str(len(items))
	
	for item in items:
		print "*WINDOW NAME: " + item['name']

	# Test getMaintenanceWindow
	print '**** TEST: getMaintenanceWindow'
	response	= mwClient.getMaintenanceWindow(windowId)
	jsonObj		= json.loads(response.text)
	description	= jsonObj.get('data', {}).get('items', {})[0].get('description', '')

	if windowDesc == description:
		print 'Description: ' + description
	else:
		print 'INCORRECT DESCRIPTION RETURNED!'

	# Test updateMaintenanceWindow
	mwTestParams['description'] = 'UPDATED DESCRIPTION'

	print '**** TEST: updateMaintenanceWindow'
	response = mwClient.updateMaintenanceWindow(windowId, mwTestParams)
	print response.text

	# Test deleteMaintenanceWindow
	print '**** TEST: deleteMaintenanceWindow'
	response = mwClient.deleteMaintenanceWindow(windowId)
	print response.text
