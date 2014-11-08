import urllib
import requests
import json
from datetime import *
import time

class Jawbone(object):
    """
    The Jawbone  API python wrapper.
    """

    def __init__(self, client_id, client_secret, redirect_uri, scope = ''):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope or 'basic_read'
        self.base_url = "https://jawbone.com/"


    def auth(self, scope=None): 
        '''
        Initial authentication for Jawbone
        '''

        params = { 
            'scope'         : scope or self.scope,
            'client_id'     : self.client_id,
            'redirect_uri'  : self.redirect_uri,
            'response_type' : 'code'  
        }

        context = {
            'base_url': self.base_url,
            'params'  : urllib.urlencode(params)
        }

        # A hard redirect to the authorize page. 
        # User would see either the login to jawbone page, 
        # or authorize page if already logged in.
        return '{base_url}auth/oauth2/auth/?{params}'.format(**context)


    def access_token(self, code, grant_type='authorization_code'):
        '''
        Get the access code for a user with a auth code.
        '''

        params = {
            'code'          : code,
            'client_id'     : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type'    : grant_type
        }

        context = {
            'base_url': self.base_url,
            'params'  : urllib.urlencode(params)
        }
 
        token_url = '{base_url}auth/oauth2/token/?{params}'.format(**context)

        res = requests.get(token_url)
        return res.json()


    def api_call(self, access_token, endpoint, **kwargs):
        '''
        Documentation URL: https://jawbone.com/up/developer/endpoints
        Example 
        endpoint: nudge/api/v.1.0/users/@me/sleep
        '''

        context = {
            'base_url': self.base_url,
            'endpoint': endpoint
        }

        api_call = '{base_url}{endpoint}'.format(**context)
        print api_call

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Host': 'jawbone.com',
            'X-Target-URI': 'https://jawbone.com',
            # 'Authorization': 'Bearer aV1SI82xvTr8IMCnyDnp4e0JNYDwJpOYii-PjrM89GJC7LrLTyKlEQ54Fw535ZnhIk3Y7hNzMDjl61urkWPYxVECdgRlo_GULMgGZS0EumxrKbZFiOmnmAPChBPDZ5JP'
            # 'Host'  : 'https://jawbone.com',
            # 'Authorization': 'Bearer {0}'.format(access_token)
            'Authorization': 'Bearer '+access_token
        }

        res = requests.get(api_call, headers=headers)

        if res.status_code == 200:
            return res.json()

        return {
            'error': res.reason, 
            'status_code': res.status_code  
        }


    def refresh_token_call(self, refresh_code):
        '''
        Get the new access code for a refresh token

        Parse the response, and update your database entries
        with the new auth credentials.
        '''

	return self.access_token(self, refresh_code, 'refresh_token')


class User(object):

    def __init__(self, jb, token):
        self.jb=jb
        self.token=token

    def get_sleep(self, date):
        try:
            # today=str(datetime.today().date())
            # today=''.join([x for x in today if x!='-'])
            sleeps=self.jb.api_call(self.token,'nudge/api/v.1.1/users/@me/sleeps?date=%s' % (date,))
            #temp hardcode
            # sleeps='{"meta": {"user_xid": "jMDIUvE60fnyHaEr3G95jA", "message": "OK", "code": 200, "time": 1415463187}, "data": {"items": [{"time_updated": 1415456257, "xid": "h8iv2zDE1c7QOkPpj10tQAgdbkITrCyx", "title": "for 8h 22m", "time_created": 1415422395, "time_completed": 1415455901, "details": {"body": 0, "sound": 11320, "smart_alarm_fire": 0, "awakenings": 2, "light": 18811, "mind": 0, "asleep_time": 1415424119, "awake_time": 1415455800, "awake": 3375, "rem": 0, "duration": 33506, "tz": "America/New_York", "quality": 88, "sunset": 0, "sunrise": 0}, "date": 20141108, "shared": true, "sub_type": 0}], "size": 1}}'

            title=sleeps['data']['items'][0]['title']
            details=sleeps['data']['items'][0]['details']
            hour=int(title[4:].split(' ')[0][:-1])
            minutes=int(title[4:].split(' ')[1][:-1])
            quality=int(details['quality'])

            return {'date':date, 'hour':hour, 'minutes':minutes, 'quality':quality}
        except:
            return {'error':'No data available for given date'}

    def get_step(self,date):
        # today=str(datetime.today().date())
        # today=''.join([x for x in today if x!='-'])

        try:
            steps=self.jb.api_call(self.token,'nudge/api/v.1.1/users/@me/moves?date=%s' %(date,))
            
            num_steps=steps['data']['items'][0]['title'].split()[0]
            num_steps=int(''.join([x for x in num_steps if x!=',']))

            details=steps['data']['items'][0]['details']
            distance=float(details['distance'])*0.000621371 #convert meters to miles
            active_time=float(details['active_time'])/60 #convert seconds to minutes
            inactive_time=float(details['inactive_time'])/60 #convert seconds to minutes
            workout_time=float(details['wo_time'])/60 #convert seconds to minutes

            return {'date':date, 'steps':num_steps, 'distance':distance, 'active_time':active_time, 'inactive_time':inactive_time, 'workout_time':workout_time}
        except:
            return {'error':'No data available for given date'}

    def is_sleep_risk(self):
        # print 'determines if theyre at sleep risk'

    def is_step_risk(self):
        print 'determines if at step risk'


client_id='VGjzSWhr3cs'
app_secret='9c46a1652607f7c155b07be591c618ce2aabfbaf'
uri='https://github.com/lilsplat'
code='mGKV_178jYxCP7r8M73hHJvZP2XktZiQb2xhklBKsBYHumXZXKCFwuCvAXd5iIEzyerH6h6H0l2-fL7a4wREe4eyzy0s7TLyCQDfEZZgjGTOLvajaxYQwcW1fdbp9foj6RAMOemI2tMGYI8mYAm0mtcq6EHVgu59Babuxo4_GDzk8lNHm2EhXb6d0YtmpUQ2'

jb = Jawbone(client_id, app_secret, uri, scope='basic_read extended_read sleep_read meal_read mood_read move_read')
# print jb.auth()
token = jb.access_token(code)
print type(token)
print jb.api_call(token['access_token'],'nudge/api/v.1.1/users/@me/sleeps')

tester=User(jb,token['access_token'])
print tester.get_step('20141107')

# print jb_extended.api_call(token,'nudge/api/v.1.1/users/@me/timezone')

