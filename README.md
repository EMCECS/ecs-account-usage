# ecs-account-usage
Creates a basic report and a Swift compatible endpoint providing information about the usage of the ECS storage per bucket owner.

## Usage

### Get the help menu:

```python3 ./account_usage.py --help```

### Basic Report:
use:

 ```python3 ./account_usage.py -u <your system_role_account_user>```

or:

```
python3 ./account_usage.py \
-e https://portal.ecstestdrive.com \
--token-endpoint https://portal.ecstestdrive.com/login \
-u <your system_role_account_user> -p <password>  \
-t temp.txt
```

 ### Launch the endpoint
 use:

 ```python3 ./account_endpoint.py -u <your system_role_account_user>```

or:

```
python3 ./account_endpoint.py \
-e https://portal.ecstestdrive.com \
--token-endpoint https://portal.ecstestdrive.com/login \
--username <your system_role_account_user> --password <password>  \
-t temp.txt -s https://swift.ecstestdrive.com \
--no-endpoint-ssl \
--port 5000

```


 ## Notes

 The token used after a sucessful login is saved in /tmp.  If you are using Windows you need to use the '-t c:\temp' to store the file in c:\temp

If you are planning to use SSL here is a good reference on how to generate a self-sign certificte
https://help.ubuntu.com/lts/serverguide/certificates-and-security.html

If you run into trouble installing the cryptographic library you may need to install the development tools for Python by running the following commmand:

Ubuntu:
```
$ sudo apt-get install build-essential libssl-dev libffi-dev python-dev
```
RHEL or Fedora:
```
$ sudo yum install gcc libffi-devel python-devel openssl-devel
```

