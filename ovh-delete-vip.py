import json
import ovh
import time
import random
import threading
import time
exec(compile(open("config.py", "rb").read(), "config.py", 'exec'))

client = ovh.Client(
    endpoint=API_ENDPOINT,               # Endpoint of API
    application_key=APPKEY,    # Application Key
    application_secret=APPSEC, # Application Secret
    consumer_key=USERKEY,       # Consumer Key
)

macwhitelist = []
ipwhitelist = []
def task_holder():
    while True:
        count = 0
        tasklistjson = client.get('/dedicated/server/' + SRV_NAME + '/task', 
            status='todo',
        )
        for taskitem in tasklistjson:
            count = count + 1
        #print("TASK REMAIN: " + str(count))
        if (count < CONN_TASK_CTRL):
            return 0
        time.sleep(2)
    
def main():
    print("This script will delete all virtualMac under " + SRV_NAME + " except following whitelist")
    print("IP White List: " + str(ipwhitelist))
    print("MAC White List: " + str(macwhitelist))
    print("To Cancel, Press Ctrl+C in 3 Seconds")
    time.sleep(3)
    macjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac')
    for macitem in macjson: 
        if str(macitem) not in macwhitelist:
            print("MAC:" + macitem)
            ipjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac/' + macitem + '/virtualAddress')
            for ipitem in ipjson:
                if str(ipitem) not in ipwhitelist:
                    thread = threading.Thread(target=task_holder)
                    thread.start()
                    thread.join()
                    print("IP:" + ipitem)
                    client.delete('/dedicated/server/' + SRV_NAME + '/virtualMac/' + macitem + '/virtualAddress/' + ipitem)
            time.sleep(1)    
if __name__ == '__main__':
    main()
