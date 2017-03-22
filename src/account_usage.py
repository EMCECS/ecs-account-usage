'''
Copyright Dell|EMC
This application provide a list of users in ECS sorted by their usage of the storage syste
'''
import sys
import operator
import logging
import getpass
import begin

from ecsclient.common.exceptions import ECSClientException
from ecsclient.client import Client


logging.basicConfig(level=logging.DEBUG)  # show only errors


class ECSConsumption(object):
    '''Get user consumption on ECS and print it to the screen'''

    def __init__(self, username, password, token_endpoint, ecs_endpoint,
                 request_timeout, verify_ssl, token_path):
        self.userrname = username
        self.password = password
        self.token_endpoint = token_endpoint

        self.ecs_endpoint = ecs_endpoint
        self.request_timeout = request_timeout
        self.verify_ssl = verify_ssl
        self.token_path = token_path

    def get_user_consumption(self):
        '''Get the users account usage information'''

        client = Client(username=self.userrname,
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
            logging.debug(namespace_id)

            # Get all the buckets for the namespace
            try:
<<<<<<< HEAD:src/account_usage.py
                buckets = client.bucket.list(namespace_id, limit=10) #  1000)
=======
                buckets = client.bucket.list(namespace_id, limit=100) #  1000)
>>>>>>> refs/remotes/origin/master:account_usage.py
            except ECSClientException:  # Secure buckets dont provide their size
                logging.warning('Error found in namespace %s\nException: %s\n skipping',
                                namespace['name'], Exception)
                continue

            for bucket in buckets['object_bucket']:
                bucket_name = bucket['name']

                try:
                    # Provide the GB consumption of the bucket been interated
                    bucket_billing = client.billing.get_bucket_billing_info(bucket_name, namespace_id)
                except ECSClientException:  # Secure buckets dont provide their size
                    logging.warning('Error found in namespace %s bucket %s\nException: %s\n skipping',
                                    bucket_name, namespace['name'], Exception)

                # Check the the current bucket's owner is registered
                user = users_dict.get(bucket['owner'])
                if user is None:  # If not owner not store, store it.
                    users_dict[bucket['owner']] = int(bucket_billing['total_size'])
                else:  # If owner is found add up the new bucket size.
                    user += int(bucket_billing['total_size'])

            logging.debug(users_dict)
        client.authentication.logout()
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

