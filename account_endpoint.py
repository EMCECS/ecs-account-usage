'''
Copyright DELL|EMC
'''

import os
import threading
import logging
import time
import begin
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

        self.user_consumption = {}  # Initate the dict that stores the usage info

    def run(self):
        while True:
            logging.info('Running forever thread')
            user_dict = self.ecsc.get_user_consumption()
            # Once data is extracted replace info with the new info.
            self.user_consumption = user_dict
            time.sleep(60 & 1000)

    def get_user_consumption(self):
        '''Returns thhe current user consumption to the main threading'''
        return self.user_consumption

# Instantiate Flask
app = Flask(__name__)

# Configure the app.config using the environmental variables otherwise use defaults
app.config['PORT'] = os.getenv('PORT', 5000)

# Global Thread
global thread

@app.route('/v1/<account>', methods=['HEAD'])
def get(account):
    x_auth_token = request.headers.get('X-Auth-Token')
    # TODO: add the Swift request that will be appended to the account usage response

    '''returns the user account information'''
    users_dic = thread.get_user_consumption()
    user = users_dic[account]
    if user is None:
        return 'error'
    else:
        resp = Response('')
        resp.headers['X-Account-Bytes-Used'] = int(int(user) * (1024 * 1024 * 1024))
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
    thread = AccountUsageThread(username,
                                password,
                                token_endpoint,
                                ecs_endpoint,
                                request_timeout,
                                verify_ssl,
                                token_path)
    thread.start()


    # context=('server.crt', 'server.key')
    logging.info('Initializing endpoint')
    app.run(debug=True,
            host='0.0.0.0',
            threaded=True,
            port=int(app.config['PORT']),
            ssl_context='adhoc'  # Use context for customer certs and keys
           )
