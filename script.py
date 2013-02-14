# =============================================================================
# script.py
#
# A class to help facilitate API calls to the 'script' service for WPM.
#
# Requires non-standard 'client' (WPM) python library to be installed.
#
# Version: 1.0
# Date: 02/13/13
# Author: Tyler Fullerton
# =============================================================================
from client import Client

class Script(Client):

	# -------------------------------------------------------------------------
	# Create a new Script object.
	#
	# key - A WPM API Key for an account
	# secret - A WPM API Secret for an account
	def __init__(self, key, secret):
		Client.__init__(self, key, secret, 'script', 'script', 'GET')

	# -------------------------------------------------------------------------
	# Override string representation of Script object.
	def __str__(self):
		# TODO: Need to update this to print 'Script', not 'Client'
		return Client.__str__(self)

	# -------------------------------------------------------------------------
	# Read script contents from a file.
	def __readScriptFile(self, fileLoc):
		contents = ''

		try:
			scriptFile	= open(fileLoc, 'r')
			contents	= scriptFile.read()
			scriptFile.close()		
		except IOError:
			print 'There is no file named', fileLoc
			contents	= ''		

		return contents
		
	# -------------------------------------------------------------------------
	# API interaction to get details of a script on the WPM platform.
	#
	# scriptId - The id of the script from the WPM platform.
	def getScript(self, scriptId):
		self.setService('script')
		self.setMethod('script/' + scriptId)
		self.setHttpMethod('GET')

		return self.call()

	# -------------------------------------------------------------------------
	# API interaction to upload a script to the WPM platform.
	#
	# params - A dictionary containing the parameters for the script.
	# fileLoc - A location on disk of a script to use.
	def uploadScript(self, params, fileLoc):
		params['scriptBody'] = self.__readScriptFile(fileLoc)

		self.setService('script')
		self.setMethod('script')
		self.setHttpMethod('POST')

		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to update a script on the WPM platform.
	#
	# scriptId - The id of the script from the WPM platform.
	# params - A dictionary containing the parameters for the script.
	# fileLoc - A location on disk of a script to use.
	def updateScript(self, scriptId, params, fileLoc):
		params['scriptBody']	= self.__readScriptFile(fileLoc)
		params['id']			= scriptId				

		self.setService('script')
		self.setMethod('script/' + scriptId)
		self.setHttpMethod('PUT')

		return self.call(params)

	# -------------------------------------------------------------------------
	# API interaction to delete a script on the WPM platform.
	#	
	# scriptId - The id of the script from the WPM platform.
	def deleteScript(self, scriptId):
		self.setService('script')
		self.setMethod('script/' + scriptId)
		self.setHttpMethod('DELETE')

		return self.call()

# -----------------------------------------------------------------------------
# Testing code
if __name__ == '__main__':

	import json

	# Variables for testing
	key 	= '[KEY]'
	secret	= '[SECRET]'

	scriptParams = {
		"name"				:"MY TEST SCRIPT",
		"description"		:"this is my test description",
		"tags"				:['api', 'testing'],
		"validationState"	:"PROCESSING",
	}

	scriptBody = '''
		var webDriver = test.openBrowser();
		test.beginTransaction();
		test.beginStep("Monitor example.com");
		webDriver.get("http://www.example.com");
		test.endStep();
		test.endTransaction();
	'''

	testFile = 'myScript.js'
	
	try:	
		testScript = open(testFile, 'w')
		testScript.write(scriptBody)
		testScript.close() 
	except IOError:
		print 'Could not create test file!'

	# Test __init__
	print '**** TEST: __init__'
	scriptClient = Script(key, secret)
	print scriptClient

	# Test __str__
	print '**** TEST: __str__'
	print scriptClient

	# Test __readScriptFile
	print '**** TEST: __readScriptFile'
	contents = scriptClient._Script__readScriptFile(testFile)
	print 'Read from file:', contents

	# Test uploadScript
	print '**** TEST: uploadScript'
	response	= scriptClient.uploadScript(scriptParams, testFile)
	jsonObj		= json.loads(response.text)
	scriptId	= jsonObj.get('data', {}).get('script', {}).get('id', '')
	print 'SCRIPT ID:', scriptId
	print response.text

	# Test updateScript
	print '**** TEST: updateScript'
	scriptParams['description'] = 'This is my UPDATED test description'
	response = scriptClient.updateScript(scriptId, scriptParams, testFile)	
	print response.text

	# Test getScript
	print '**** TEST: getScript'
	response = scriptClient.getScript(scriptId)
	print response.text

	# Test deleteScript
	print '**** TEST: deleteScript'
	response = scriptClient.deleteScript(scriptId)
	print response.text
