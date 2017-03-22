'''
Copyright DELL|EMC
'''

import os
import threading
import logging
import time
import begin
import requests
from flask import Flask, Response, request
from account_usage import ECSConsumption


logging.basicConfig(level=logging.DEBUG)

class AccountUsageThread(threading.Thread):
    '''Get the user information, runs a thread to keep it updated
    and provides an endpoint
    '''

    def __init__(self,
                 username,
                 password,
                 token_endpoint,
                 ecs_endpoint,
                 request_timeout,
                 verify_ssl,
                 token_path):
        threading.Thread.__init__(self)
        logging.info('Initializing thread')
        self.ecsc = ECSConsumption(username,
                                   password,
                                   token_endpoint,
                                   ecs_endpoint,
                                   request_timeout,
                                   verify_ssl,
                                   token_path)

        self.user_consumption = {}   # Initate the dict that stores the usage info

    def run(self):
        while True:
            logging.info('Running forever thread')
            user_dict = self.ecsc.get_user_consumption()
            # Once data is extracted replace info with the new info.
            self.user_consumption = user_dict
            time.sleep(300 & 1000)
            break  # TODO: remove after debugging

    def get_user_consumption(self):
        '''Returns thhe current user consumption to the main threading'''
        return self.user_consumption


# Instantiate and configure Flask
app = Flask(__name__)
app.config['PORT'] = os.getenv('PORT', 9025)


@app.route('/v1/<account>', methods=['HEAD'])
def head(account):
    x_auth_token = request.headers.get('X-Auth-Token')
    r = requests.head('{0}:9025/v1/{1}'.format(_ecs_endpoint, account),
                      headers={'X-Auth-Token':x_auth_token}, verify=_verify_ssl)

    users_dic = thread.get_user_consumption()  # return users account info
    user = users_dic.get(account)
    if user is None:
        return 'error'
    else:
        resp = Response(r.content, r.status_code)
        newheader = {}
        for k, v in r.headers.items():
            newheader[k] = v

        newheader['X-Account-Bytes-Used'] = int(users_dic[account]) * (1024 * 1024 * 1024)
        resp.headers = newheader
        return resp

@app.route('/v1/<account>', methods=['GET'])
def get(account):
    x_auth_token = request.headers.get('X-Auth-Token')
    
    r = requests.get('{0}:9025/v1/{1}'.format(_ecs_endpoint, account),
                     headers={'X-Auth-Token':x_auth_token}, verify=_verify_ssl)

    resp = Response(r.content, r.status_code)
    newheader = {}
    for k, v in r.headers.items():
        newheader[k] = v
    resp.headers = newheader
    # resp = Response('')
    # resp.headers = r.headers
    # resp.data = r.text
    return resp

# if __name__ == "__main__":
if begin.start():
    pass

@begin.start(auto_convert=False)
def run(username='admin',
        password='password',
        token_endpoint='https://portal.ecstestdrive.com/login',
        ecs_endpoint='https://portal.ecstestdrive.com',
        request_timeout=15,
        verify_ssl=False,
        token_path='/tmp'):
    '''
    Creates an endpoint for Swift the provide account usage header X-Account-Bytes-Used.
    '''
    # AccountEndpoint()

    logging.info('Initializing thread to capture usage')

    global thread
    thread = AccountUsageThread(username,
                                password,
                                token_endpoint,
                                ecs_endpoint,
                                request_timeout,
                                verify_ssl,
                                token_path)
    thread.start()

    global _ecs_endpoint
    _ecs_endpoint = ecs_endpoint

    global _verify_ssl
    _verify_ssl = verify_ssl

    # context=('server.crt', 'server.key')
    logging.info('Initializing endpoint')
    app.run(debug=True,
            host='0.0.0.0',
            threaded=True,
            port=int(app.config['PORT']),
            ssl_context='adhoc'  # Use context for customer certs and keys
           )
