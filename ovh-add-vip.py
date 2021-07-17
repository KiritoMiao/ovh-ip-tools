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
ipalreadyhavemaclist = []
ipblacklist = []
cidrblacklist = []
cidrtargetmode = False
cidrtarget = ""
def task_holder():
    while True:
        count = 0
        tasklistjson = client.get('/dedicated/server/' + SRV_NAME + '/task', 
            status='todo',
        )
        for taskitem in tasklistjson:
            count = count + 1
#        print("TASK REMAIN: " + str(count))
        if (count < CONN_TASK_CTRL):
            return 0
        time.sleep(2)
    
def main():
    macjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac')
    for macitem in macjson:
        iplistjson = client.get('/dedicated/server/' + SRV_NAME + '/virtualMac/' + macitem + '/virtualAddress')
        for ipitem in iplistjson:
            ipalreadyhavemaclist.append(ipitem)
    if cidrtargetmode == False:
        print("This script will add virtualMac for all additional ip address under " + SRV_NAME + "except following blacklist")
        print("This Script is undet normal operation mode")
        print("IP Black List: " + str(ipblacklist))
        print("CIDR Black List: " + str(cidrblacklist))
        print("IP Already have MAC: " + str(ipalreadyhavemaclist))
        print("To Cancel, Press Ctrl+C in 3 Seconds")
        time.sleep(3)
        iprangejson = client.get('/dedicated/server/' + SRV_NAME + '/ips')
        for iprangeitem in iprangejson:
            print("CIDR: " + iprangeitem)
            if '/32' not in iprangeitem and ':' not in iprangeitem and iprangeitem not in cidrblacklist:
                for ip in ipaddress.IPv4Network(iprangeitem):
                    thread = threading.Thread(target=task_holder)
                    thread.start()
                    thread.join()
                    if str(ip) not in ipalreadyhavemaclist and str(ip) not in ipblacklist:
                        print("IP: " + str(ip))
                        client.post('/dedicated/server/' + SRV_NAME + '/virtualMac', 
                            ipAddress=str(ip),
                            type='ovh',
                            virtualMachineName=str(ip),
                        )
            else:
                print("This IP range does not support by this script")  
    else:
        print("This Script is CIDR Target operation mode")
        print("IP Black List: " + str(ipblacklist))
        print("CIDR Black List Disabled")
        print("Under this mode script will not check compability of this CIDR")
        for ip in ipaddress.IPv4Network(cidrtarget):
            thread = threading.Thread(target=task_holder)
            thread.start()
            thread.join()
            if str(ip) not in ipalreadyhavemaclist and str(ip) not in ipblacklist:
                print("IP: " + str(ip))
                client.post('/dedicated/server/' + SRV_NAME + '/virtualMac',                
                    ipAddress=str(ip),
                    type='ovh',
                    virtualMachineName=str(ip),
                )





 
if __name__ == '__main__':
    main()
