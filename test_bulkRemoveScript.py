from script import Script
import json

key		= '220.1.dHlsZXI.dHlsZXI.e7DE31kYiQ2D0JZP6UmRGsGboKQYCDIal1INCg'
secret	= 'tXBGIBK5'
client	= Script(key, secret)

print 'client:', client

response	= client.getScript('')
jsonObj		= json.loads(response.text)
scripts		= jsonObj.get('data', {}).get('items', [])
ids			= []

for script in scripts:
	scriptName	= script.get('name', '')	

	print 'name:', scriptName

	if scriptName.startswith('script_cs'):
		scriptId = script.get('id', '')
		response = client.deleteScript(scriptId)
		print '*** DELETED:', scriptId, '-', scriptName
