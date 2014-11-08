from bottle import route, run, template
from jawbone import *

# @route('/hello/<name>')
# def index(name):
#     return template('<b>Hello {{name}}</b>!', name=name)
#     #the host has to match the host o_o
# # run(host='162.218.234.58', port=8080)

# run(host='localhost', port=8080, debug=True)


@route('/hello')
def hello():
	client_id='VGjzSWhr3cs'
	app_secret='9c46a1652607f7c155b07be591c618ce2aabfbaf'
	uri='https://github.com/lilsplat'
	code='mGKV_178jYxCP7r8M73hHJvZP2XktZiQkY1HWlVNvbgHumXZXKCFwuCvAXd5iIEzyerH6h6H0l2-fL7a4wREe4eyzy0s7TLyCQDfEZZgjGTOLvajaxYQwcW1fdbp9foj6RAMOemI2tMGYI8mYAm0mtcq6EHVgu59Babuxo4_GDzk8lNHm2EhXb6d0YtmpUQ2'
	
	jb = Jawbone(client_id, app_secret, uri, scope='basic_read extended_read sleep_read meal_read mood_read move_read')
	# print jb.auth()
	token = jb.access_token(code)
	# print jb.api_call(token['access_token'],'nudge/api/v.1.1/users/@me/goals')

	tester=User(jb,token['access_token'])
	# print tester.is_at_risk()
	return tester.is_at_risk()

# run(host='localhost', port=8080, debug=True)
run(host='10.240.112.192',port=8080)