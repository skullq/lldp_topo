from netmiko import ConnectHandler
import re

def get_lldp_info(hostname, username, password):
    cisco_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': hostname,
        'username': username,
        'password': password,
        'timeout' : 15
    }
    try:
        connection = ConnectHandler(**cisco_device)
        lldp_output = connection.send_command('show lldp neighbors detail')
        connection.disconnect()
        return lldp_output
    except Exception as e:
        return f"Error: {str(e)}"

def parse_lldp_info(lldp_info):
    devices = re.findall(r'System Name: (.+?)\n', lldp_info)
    ports = re.findall(r'Port id: (.+?)\n', lldp_info)

    return list(zip(devices, ports))

def create_network_topology(lldp_info):
    topology = {}

    for device, port in lldp_info:
        if device not in topology:
            topology[device] = []

        topology[device].append(port)

    return topology

switches = [
    {'hostname': '10.1.1.1', 'username': 'cisco', 'password': 'cisco'},
    {'hostname': '3.3.3.3', 'username': 'cisco', 'password': 'cisco'},
    {'hostname': '1.1.1.1', 'username': 'cisco', 'password': 'cisco'}
]

topology = {}

for switch in switches:
    lldp_info = get_lldp_info(switch['hostname'], switch['username'], switch['password'])
    lldp_info = parse_lldp_info(lldp_info)
    switch_topology = create_network_topology(lldp_info)

    for device, ports in switch_topology.items():
        if device not in topology:
            topology[device] = []

        topology[device].extend(ports)

print(topology)
root@Docker:/Docker-images# cat lldp-thread.py 
from netmiko import ConnectHandler
from threading import Thread
import re

def get_lldp_info(switch):
    connection = ConnectHandler(device_type='cisco_ios_telnet', ip=switch['ip'], username=switch['username'], password=switch['password'])
    lldp_output = connection.send_command('show lldp neighbors detail')
    connection.disconnect()

    devices = re.findall(r'System Name: (.+?)\n', lldp_output)
    ports = re.findall(r'Port id: (.+?)\n', lldp_output)

    return list(zip(devices, ports))

def worker(switch, topology):
    lldp_info = get_lldp_info(switch)

    for device, port in lldp_info:
        if device not in topology:
            topology[device] = []

        topology[device].append(port)

switches = [
    {'ip': '10.1.1.1', 'username': 'cisco', 'password': 'cisco'},
    {'ip': '3.3.3.3', 'username': 'cisco', 'password': 'cisco'},
    {'ip': '1.1.1.1', 'username': 'cisco', 'password': 'cisco'}
]

topology = {}

threads = []
for switch in switches:
    thread = Thread(target=worker, args=(switch, topology))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(topology)
