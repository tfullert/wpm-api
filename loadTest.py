# =============================================================================
# loadTest.py
#
# A class to facilitate API calls to WPMs load testing platform.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 12/06/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class LoadTest(Client):

	# -------------------------------------------------------------------------
	# Constant variables used to define load test regions.
	US_EAST			= 0		# Washington, D.C.
	US_WEST			= 1		# San Francisco
	EU_WEST			= 2		# Dublin
	AP_SOUTHEAST	= 3		# Singapore
	AP_NORTHEAST	= 4		# Tokyo
	SAO_PAULO		= 5		
	OREGON			= 6
	SYDNEY			= 7
	MULTI_REGION	= 8		# Multi-region support

	# -------------------------------------------------------------------------
	# Create a new LoadTest object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'load', '', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of LoadTest object.
	def __str__(self):
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# API interaction to echo a message back to the caller.
	# 
	# message - A string to echo back (no spaces).
	def echoMessage(self, message):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/echo/' + message)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to find out the username associated with API key/secret.
	def whoAmI(self):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/whoami')
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get a list of tests as JSON response.
	# 
	# params - Dictonary of parameters to API call:
	#  * limit: The max number of tests to return.
	#  * callback: A javaScript function to send results to.
	def getListOfTestsAsJSON(self, params):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/list/mostRecent')
		self.setHttpMethod('GET')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get a list of tests.
	# 
	# params - Dictionary list of parameters.
	#  * limit: The number of tests to return.
	def getListOfTests(self, limit):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/list')
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to add tag to load test.
	#
	# loadTestId - Id of the load test to tag.
	# tagName - The tag to apply to the load test.
	def addTag(self, loadTestId, tagName):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/' + str(loadTestId) + '/tag/' + tagName)
		self.setHttpMethod('PUT')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to remove tag from load test.
	# 
	# loadTestId - The ID of the test to tag.
	# tagName - The tag to remove from the load test.
	def removeTag(self, loadTestId, tagName):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/' + str(loadTestId) + '/tag/' + tagName)
		self.setHttpMethod('DELETE')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get a load test.
	#
	# loadTestId - The ID of the load test to get.
	def getLoadTest(self, loadTestId):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/id/' + str(loadTestId))
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to delete a load test.
	# 
	# loadTestId - The ID of the load test to delete.
	def deleteLoadTest(self, loadTestId):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/' + str(loadTestId) + '/delete')
		self.setHttpMethod('DELETE')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to pause a load test.
	#
	# loadTestId - The ID of the load test to pause.
	def pauseLoadTest(self, loadTestId):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/' + str(loadTestId) + '/pause')
		self.setHttpMethod('PUT')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to resume a load test.
	#
	# loadTestId - The ID of the load test to resume.
	def resumeLoadTest(self, loadTestId):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/' + str(loadTestId) + '/resume')
		self.setHttpMethod('PUT')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to schedule a load test.
	# 
	# params - Dictionary containing parameters to post.
	#  * name: Name of the load test.
	#  * region: The region(s) to run from.
	#  * start: Time to start the load test.
	#  * scripts: Scripts to run for the load test.
	#  * overrideCode: An override code to use for the load test.
	#  * parts: The test plan.
	def scheduleLoadTest(self, params):
		self.setService('load')
		self.setMethod(self.wpmAPIVersion + '/schedule')
		self.setHttpMethod('POST')
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

	# Create parameters for load test
	ltName		= ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
	futureStart	= datetime.now() + timedelta(minutes=900)	
	startDate	= futureStart.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
	testPlan	= [{"duration" : 30, "maxUsers" : 10, "type" : 'RAMP'}]
	scripts		= [{"percentage" : 100, "scriptId" : '8839490a355b49ff97188662d354a0dc'}]
	params		= {}

	# TODO: This load test ID is for testing the API calls that expect a load test to already be created.  
	# I recommend setting up a load test in your account that is available for testing purposes.  
	# Then set the loadTestId value to the load test ID for that completed load test.  This value
	# will be overwritten by the test that schedules a load test.
	# loadTestId = '158023'

	# Test __init__
	print '**** TEST: __init__'
	ltClient = LoadTest(key, secret)
	print ltClient

	# Test __str__
	print '**** TEST: __str__'
	print ltClient

	# Test echoMessage
	print '**** TEST: echoMessage'
	response = ltClient.echoMessage('TEST_MESSAGE')
	print response.text

	# Test whoAmI
	print '**** TEST: whoAmI'
	response	= ltClient.whoAmI()
	jsonObj		= json.loads(response.text)
	username	= jsonObj.get('data', {}).get('username', '')
	print 'Username: ' + username

	params.clear()
	params = {'limit' : '5', 'callback'	: 'myFunc'}
		
	# Test getListOfTestsAsJSON
	print '**** TEST: getListOfTestsAsJSON'
	response = ltClient.getListOfTestsAsJSON(params)
	print 'Callback: ' + response.text

	params.clear()
	params = {'limit' : '5'}

	# Test getListOfTests
	print '**** TEST: getListOfTests'
	response	= ltClient.getListOfTests(params)
	jsonObj		= json.loads(response.text)
	tests		= jsonObj.get('data', {}).get('items', [])

	print 'TESTS:'
	for test in tests:
		print '** ' + test['name']

	params.clear()	
	params = {
		'name'			: ltName,
		'region'		: ltClient.US_EAST,
		'start'			: startDate,
		'scripts'		: scripts,
		'overrideCode'	: '',
		'parts'			: testPlan,
	}

	# Test scheduleLoadTest
	print '**** TEST: scheduleLoadTest'
	print 'Scheduling load test with params:'
	response	= ltClient.scheduleLoadTest(params)
	jsonObj		= json.loads(response.text)
	state		= jsonObj.get('data', {}).get('loadTest', {}).get('state', '')
	loadTestId	= jsonObj.get('data', {}).get('loadTest', {}).get('id', '')

	if state == 'SCHEDULED':
		print 'Load test successfully scheduled.'
	else:
		print 'ERROR: Load test was not scheduled!'
	print response.text

	# Test getLoadTest
	print '**** TEST: getLoadTest'
	response	= ltClient.getLoadTest(loadTestId)
	jsonObj		= json.loads(response.text)
	state		= jsonObj.get('data', {}).get('loadTest', {}).get('state', '')
	print 'Load test has state: ' + state

	# Test addTag
	print '**** TEST: addTag'
	response = ltClient.addTag(loadTestId, 'MY_TAG')
	print response.text

	# Test removeTag
	print '**** TEST: removeTag'
	response = ltClient.removeTag(loadTestId, 'MY_TAG')
	print response.text

	# Test pauseLoadTest
	print '**** TEST: pauseLoadTest'
	response = ltClient.pauseLoadTest(loadTestId)
	print response.text

	# Test resumeLoadTest
	print '**** TEST: resumeLoadTest'
	response = ltClient.resumeLoadTest(loadTestId)
	print response.text

	# Test deleteLoadTest
	print '**** TEST: deleteLoadTest'
	response = ltClient.deleteLoadTest(loadTestId)
	print response.text
