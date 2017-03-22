# ecs-account-usage
Creates a basic report and a Swift compatible endpoint providing information about the usage of the ECS storage per bucket owner.

## Usage

### Get the help menu:

```python ./account_usage.py --help```

### Basic Report:
use:

 ```python .\account_usage.py -u <your system_role_account_user```

or:

```
python .\account_usage.py
-e https://portal.ecstestdrive.com --token-endpoint https://portal.ecstestdrive.com/login -u <your system_role_account_user> -p <password>  -t temp.txt
```

 ### Launch the endpoint
 use:

 ```python .\account_endpoint.py -u <your system_role_account_user>```

or:

```
python .\account_endpoint.py -e https://portal.ecstestdrive.com --token-endpoint https://portal.ecstestdrive.com/login -u <your system_role_account_user> -p <password>  -t temp -s https://swift.ecstestdrive.com

```


 ## Notes

 The token used after a sucessful login is saved in /tmp.  If you are using Windows you need to use the '-t c:\temp' to store the file in c:\temp

