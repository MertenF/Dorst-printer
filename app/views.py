from flask import request, Response

from app import app, config, main
import logging


@app.route('/cgi-bin/epos/service.cgi', methods=['POST', 'GET'])
def epos_service_cgi():
    if request.method == 'GET':
        return 'GET requests not supported. Use POST request with EPOS-XML'


    print('Data:')
    print(request.data.decode('utf-8'))
    print('Data END')
    return_data = main.handle_request(request.data.decode('utf-8'))
    return Response(return_data, mimetype='text/xml')



@app.route('/')
def hello_world():
    return 'Nothing to see here'

@app.route('/error')
def error():
    s = 'This is an error message'
    logging.error(s)
    return s

@app.route('/warning')
def warning():
    s = 'This is a warning message'
    logging.warning(s)
    return s

@app.route('/info')
def info():
    s = 'This is an info message'
    logging.info(s)
    return s