# =============================================================================
# instantTest.py
#
# A class to help facilitate API calls to the 'Instant Test' functionality
# of WPM.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 12/05/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class InstantTest(Client):

	# -------------------------------------------------------------------------
	# Create a new InstantTest object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'tools', '', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of Monitor object.
	def __str__(self):
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# API interaction to create a job for the Instant Test tool.
	#
	# params - Dictionary containing the details of the test.
	#   * url: URL to test.
	#   * callback: Callback URL to post results to.
	def createInstantTestJob(self, params):
		self.setService('tools')
		self.setMethod('instanttest/' + self.wpmAPIVersion)
		self.setHttpMethod('POST')
		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to get results of an instant test job.
	#
	# testId - ID value of an instant test job. 
	def getInstantTestJob(self, testId):
		self.setService('tools')
		self.setMethod('instanttest/' + self.wpmAPIVersion + '/' + testId)
		self.setHttpMethod('GET')
		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to get results of an instant test job by location.
	#
	# testId - ID value of an instant test job.
	# location - Location where test was run from.
	def getInstantTestJobByLocation(self, testId, location):
		self.setService('tools')
		self.setMethod('instanttest/' + self.wpmAPIVersion + '/' + testId + '/' + locationId)
		self.setHttpMethod('GET')
		return self.call()
	
# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import json
	import time
	import string
	import random
	from tester import Tester

	# Variables for testing	
	key		= Tester.wpmAPIKey
	secret	= Tester.wpmAPISecret

	testParams = {
		'url'			: 'www.neustar.biz',
		'callback'		: 'www.example.com',
	}

	# Test __init__
	print '**** TEST: __init__'
	itClient = InstantTest(key, secret)
	print itClient

	# Test __str__
	print '**** TEST: __str__'
	print itClient

	# Test createInstantTestJob
	print '**** TEST: createInstantTestJob'
	response	= itClient.createInstantTestJob(testParams)
	jsonObj		= json.loads(response.text)
	jobId		= jsonObj.get('data', {}).get('items', {}).get('id', '')
	location	= jsonObj.get('data', {}).get('items', {}).get('locations', [])[0].get('location', '')
	locationId	= jsonObj.get('data', {}).get('items', {}).get('locations', [])[0].get('id', '')
	print 'Job ID: ', jobId
	print 'Location ID: ', locationId
	print 'Location: ', location

	# Test getInstantTestJob
	print '**** TEST: getInstantTestJob'
	response	= itClient.getInstantTestJob(jobId)
	jsonObj		= json.loads(response.text)
	jobs		= jsonObj.get('data', {}).get('items', {})

	for job in jobs:
		location	= job['location']
		status		= job['status']
		print 'Status of job from ' + location + ' is ' + status

	# Test getInstantTestJobByLocation
	print '**** TEST: getInstantTestJobByLocation'
	response	= itClient.getInstantTestJobByLocation(jobId, location)
	jsonObj		= json.loads(response.text)
	jobStatus	= jsonObj.get('data', {})[0].get('status', '')
	print "STATUS: " + jobStatus
