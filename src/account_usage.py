'''
Copyright Dell|EMC
This application provide a list of users in ECS sorted by their usage of the storage syste
'''
import operator
import logging
import getpass
import begin
import os

from ecsclient.common.exceptions import ECSClientException
from ecsclient.client import Client


logging.basicConfig(level=logging.ERROR)  # show only errors


class ECSConsumption(object):
    '''Get user consumption on ECS and print it to the screen'''

    def __init__(self, username, password, token_endpoint, ecs_endpoint,
                 request_timeout, verify_ssl, token_path):
        self.username = username
        self.password = password
        self.token_endpoint = token_endpoint

        self.ecs_endpoint = ecs_endpoint
        self.request_timeout = request_timeout
        self.verify_ssl = verify_ssl
        self.token_path = token_path

    def get_user_consumption(self):
        '''Get the users account usage information'''

        client = Client(username=self.username,
                        password=self.password,
                        token_endpoint=self.token_endpoint,
                        ecs_endpoint=self.ecs_endpoint,
                        request_timeout=self.request_timeout,
                        verify_ssl=self.verify_ssl,
                        token_path=self.token_path, version='3')


        namespaces = client.namespace.list()  # Get all the namespaces in the system
        users_dict = {}

        for namespace in namespaces['namespace']:
            namespace_id = namespace['id']
            namespace_name = namespace['name']
            logging.debug(namespace_id)

            namespace_info = client.billing.get_namespace_billing_info(namespace_id)
            users_dict[namespace_name] = int(namespace_info['total_size'])
            
            logging.debug(users_dict)
        client.authentication.logout()

        if os.path.exists(self.token_path): #  clean old token
            os.remove(self.token_path)

        return users_dict


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
    Creates a simple report using the CLI
    '''

    if password is 'password':
        password = getpass.getpass(prompt='Password: ', stream=None)

    ecs = ECSConsumption(username, password, token_endpoint, ecs_endpoint, request_timeout,
                         verify_ssl, token_path).get_user_consumption()

    # Display users and utilization
    print('\n{0:50} {1:5} GB'.format('users', 'consumption'))
    for key, value in sorted(ecs.items(), key=operator.itemgetter(1)):
        print('{0:50} {1:>5} GB'.format(key, value))

