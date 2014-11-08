from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)
    #the host has to match the host o_o
run(host='162.218.234.58', port=8080)
