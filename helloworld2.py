from bottle import route, run, template, request
from threading import Timer
from twilio.rest import TwilioRestClient 
import json

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)
    #the host has to match the host o_o
    
@route('/makevillage')
def makevillage():
    print "yeah"
    print request.query
    print request.query.thedata
    thedata = json.loads(request.query.thedata)
    print thedata
    print thedata[1]
    print request.json
    return "yeah2"
    #the host has to match the host o_o

def function_to_be_scheduled():
   print "hey"  
     
interval = 0.1   #interval (4hours)
Timer(interval, function_to_be_scheduled).start() 
 
# put your own credentials here 
ACCOUNT_SID = "ACd7cd0ce30637010f7abadadaba2b64bf" 
AUTH_TOKEN = "c6087a85b088aef44d9989456134d1e9" 
 
#client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
#client.messages.create(
#	to="16179718435", 
#	from_="+15204471156", 
#	body="Night :)",  
#)

run(host='162.218.234.58', port=8080)





