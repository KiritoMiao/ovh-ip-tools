# OVH IP Tools
Automatic config OVH Failover IP with a Virtual MAC for VM


## Config File
API_ENDPOINT = "ovh-eu" // Do not change this unless you know what are you doing

// Go to this webpage to get your token (For api region other than eu, your url may vary) https://eu.api.ovh.com/createToken/

APPKEY = '' 

APPSEC = ''

USERKEY = '' 

SRV_NAME = '' // Server's NET name

CONN_TASK_CTRL = 2 // Concurrency number, unless you understand what this is, otherwise use the default value.

## Usage

### Print IP-MAC Relationship
python ovh-print-vip.py

### Add Virtual MAC for all IP
python ovh-add-vip.py

### Delete Virtual MAC for all IP
python ovh-delete-vip.py


## Advance Usage
Read comment in ovh-delete-vip.py and ovh-add-vip.py.
