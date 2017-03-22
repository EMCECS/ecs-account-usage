# ecs-account-usage
Creates a basic report and a Swfit compatible endpoint providing information about the usage of the ECS storage per bucket owner.

## Usage

Get the help menu:

```python ./account_usage.py --help```

To launch the basic report:

 ```python .\account_usage.py -u <your system_role_account_user```

 To launch the endpoint:

 ```python .\account_endpoint.py -u <your system_role_account_user```

 ## Notes

 The token used after a sucessful login is saved in /tmp.  If you are using Windows you need to use the '-t c:\temp' to store the file in c:\temp


