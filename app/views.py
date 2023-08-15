import re

from flask import request, Response

from app import app, config, main
import logging


@app.route('/cgi-bin/epos/service.cgi', methods=['POST', 'GET'])
def epos_service_cgi():
    if request.method == 'GET':
        return 'GET requests not supported. Use POST request with EPOS-XML'

    data = request.data.decode('utf-8')
    if re.search('snacks', data, re.IGNORECASE):
        print('snacks')
        return_data = main.request_snackkot(data)
    elif re.search('doorgeef', data, re.IGNORECASE):
        print('doorgeef')
        return_data = main.request_doorgeef(data)
    else:
        print('Unknown')
        return_data = main.request_unkown(data)

    print('RETURNING DATA')
    return Response(return_data, mimetype='text/xml')



@app.route('/')
def hello_world():
    s = 'Nothing to see here\n'
    s += request.host
    return s

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