from flask import request, Response

from app import app, config, main


@app.route('/')
def hello_world():
    return 'Nothing to see here'


@app.route('/cgi-bin/epos/service.cgi', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return 'GET requests not supported. Use POST request with EPOS-XML'


    print('Data:')
    print(request.data.decode('utf-8'))
    print('Data END')
    return_data = main.handle_request(request.data.decode('utf-8'))
    return Response(return_data, mimetype='text/xml')