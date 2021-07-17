import json
import ovh
import time
import random
import threading
import time
import ipaddress
exec(compile(open("config.py", "rb").read(), "config.py", 'exec'))

client = ovh.Client(
    endpoint=API_ENDPOINT,               # Endpoint of API
    application_key=APPKEY,    # Application Key
    application_secret=APPSEC, # Application Secret
    consumer_key=USERKEY,       # Consumer Key
)
def task_holder():
    while True:
        count = 0
        tasklistjson = client.get('/dedicated/server/' + SRV_NAME + '/task', 
            status='todo',
        )
        for taskitem in tasklistjson:
            count = count + 1
        print("TASK REMAIN: " + str(count))
        if (count < 3):
            return 0
        time.sleep(2)
    
def main():
    macjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac')
    for macitem in macjson:
        iplistjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac/' + macitem + '/virtualAddress')
        for ipitem in iplistjson:
            print(ipitem + " " + macitem)   
if __name__ == '__main__':
    main()
