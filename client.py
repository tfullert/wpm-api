# =============================================================================
# client.py
#
# A class to help facilitate API calls for WPM.
#
# Requires non-standard 'requests' python library to be installed.
#
# Version: 1.0
# Date: 02/11/13
# Author: Tyler Fullerton
# =============================================================================
import md5
import time
import json
import string
import requests

class Client:

	wpmAPIBase		= 'http://api.neustar.biz/performance/'
	wpmAPIVersion	= '1.0'

	debug			= 1
	
	# -------------------------------------------------------------------------
	# Create a new Client object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	# service - API service to perform (monitor, load, rum, tools, maintenance)
	# method - API method to perform (beacon, instanttest, list, etc.)
	# httpMethod - HTTP method required by the API service/method (POST, GET, PUT, DELETE)
	def __init__(self, key, secret, service='', method='', httpMethod='GET'):
		self.key		= key.encode('utf-8')
		self.secret		= secret.encode('utf-8')
		self.service	= service
		self.method		= method
		self.httpMethod	= string.upper(httpMethod)

	# -------------------------------------------------------------------------
	# Override string representation of Client object.
	def __str__(self):
		return '[%s: %s, %s, %s, %s, %s]' % (self.__class__.__name__, self.key, self.secret, self.service, self.method, self.httpMethod)

	# -------------------------------------------------------------------------
	# Perform an HTTP DELETE. 
	def __doDelete(self, url):
		return requests.delete(url)

	# -------------------------------------------------------------------------
	# Perform an HTTP GET.
	def __doGet(self, url):
		return requests.get(url)		

	# -------------------------------------------------------------------------
	# Perform an HTTP POST.
	def __doPost(self, url, data):
		return requests.post(url, data=json.dumps(data), headers={'Content-Type':'application/json'})

	# -------------------------------------------------------------------------
	# Perform an HTTP PUT.
	def __doPut(self, url, data):
		return requests.put(url, data=json.dumps(data), headers={'Content-Type':'application/json'})

	# -------------------------------------------------------------------------
	# Construct URL.
	def __constructURL(self, data=''):

		# For some odd reason, the 'script' method does not require an API version number		
		url		= Client.wpmAPIBase + self.service + '{}'.format('' if self.method.startswith('script') else '/' + Client.wpmAPIVersion)
		url		= url + '{}'.format('/' + self.method if self.method else '')
		url		= url + '?apikey=' + self.key + '&sig=' + self.signature() 

		# Attach additional parameters for GET requests
		if self.httpMethod == 'GET' and data:
			url = url + "&" + "&".join("%s=%s" % item for item in data.items())

		if self.debug:
			print 'URL:', url
		
		return url
	
	# =========================================================================
	# Setters for Instance variables.
	def setKey(self, key):
		self.key = key

	def setSecret(self, secret):
		self.secret = secret
	
	def setService(self, service):
		self.service = service

	def setMethod(self, method):
		self.method = method

	def setHttpMethod(self, httpMethod):
		self.httpMethod = string.upper(httpMethod)

	# -------------------------------------------------------------------------
	# Create a signature for API calls.
	def signature(self):
		return md5.new(self.key + self.secret + str(int(time.time())).encode('utf-8')).hexdigest()

	# -------------------------------------------------------------------------
	# Marshall the call to the API.
	# 
	# data - parameter should be provided when performing a POST or a PUT
	def call(self, data=''):
		url		= self.__constructURL(data)		
		results = ''
		
		try:
			if self.httpMethod == 'GET':
				results = self.__doGet(url)
			elif self.httpMethod == 'POST':			
				results = self.__doPost(url, data)
			elif self.httpMethod == 'DELETE':
				results = self.__doDelete(url)
			elif self.httpMethod == 'PUT':
				results = self.__doPut(url, data)
			else:
				print 'Invalid httpMethod', self.httpMethod
		except requests.RequestException as e:
			print 'Client error:', str(e)
		except requests.Timeout as e:
			print 'Request timeout:', str(e)
			
		return results

# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import random

	# Variables for testing
	key 	= '[KEY]'
	secret	= '[SECRET]'

	svcName	= ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
	params 	= {
		'name'			: svcName,
		'description'	: '',
		'interval'		: '60',
		'locations'		: 'london',
		'browser'		: 'FF',
		'active'		: '0',
		'testScript'	: 'default_script',
	}

	uParams	= {'interval':'10'}

	# Test __init__
	print '**** TEST: __init__'	
	client1 = Client(key, secret, 'monitor', 'locations', 'GET')
	client2 = Client(key, secret, httpMethod='put')
	client3 = Client(key, secret, service='monitor', httpMethod='get', method='locations')	
	client4 = Client(key, secret, method='locations')
	
	# Test __str__
	print '**** TEST: __str__'
	print client1
	print client2
	print client3
	print client4
	
	# Test signature
	print '**** TEST: signature'
	print client3.signature()

	# Test call	
	print '**** TEST: call'
	print client3.call()

	# Test setters
	print '**** TEST: setters'
	print client1
	client1.setKey('fakeKey')
	client1.setSecret('fakeSecret')
	client1.setService('fakeService')
	client1.setMethod('fakeMethod')
	client1.setHttpMethod('fakeHttpMethod')
	print client1

	# NOTE: Mangled names used for internal methods/attributes (i.e. __methodName).  
	# You would normally not use these methods as they are meant to be internal to the class.
	
	# Test __constructURL
	print '**** TEST: __constructURL'
	client3.setService('monitor')
	client3.setHttpMethod('get')
	client3.setMethod('locations')
	print client3._Client__constructURL()

	# And...Test __constructURL with parameters
	print '**** TEST: __constructURL (with params)'
	client3.setService('monitor')
	client3.setHttpMethod('get')
	client3.setMethod('locations')
	print client3._Client__constructURL({'key1':'value1','key2':'value2'})
	
	# Test __doPost
	print '**** TEST: __doPost'
	client3.setService('monitor')
	client3.setHttpMethod('POST')
	client3.setMethod('')
	print client3
	rsp		= client3._Client__doPost(client3._Client__constructURL(), params)
	jsonObj = json.loads(rsp.text)
	svcID	= jsonObj.get('data', {}).get('items', {}).get('id', '')
	print rsp.text	

	# Test __doGet
	print '**** TEST: __doGet'
	client3.setService('monitor')
	client3.setHttpMethod('get')
	client3.setMethod(svcID)
	print client3
	rsp		= client3._Client__doGet(client3._Client__constructURL())
	print rsp.text

	# Test __doPut
	print '**** TEST: __doPut'
	client3.setService('monitor')
	client3.setHttpMethod('put')
	client3.setMethod(svcID)
	print client3
	rsp		= client3._Client__doPut(client3._Client__constructURL(), uParams)
	print rsp.text

	# Test __doDelete
	print '**** TEST: __doDelete'
	client3.setService('monitor')
	client3.setHttpMethod('delete')
	client3.setMethod(svcID)
	print client3
	rsp		= client3._Client__doDelete(client3._Client__constructURL())
	print rsp.text
