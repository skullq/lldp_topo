root@Docker:/Docker-images# time(python3 lldp.py)
{'r3': ['Et0/1', 'Et0/0'], 'r1': ['Et0/1'], 'r5': ['Et0/0']}

real	0m8.886s
user	0m0.089s
sys	0m0.021s


root@Docker:/Docker-images# time(python3 lldp-thread.py)
{'r3': ['Et0/1', 'Et0/0'], 'r1': ['Et0/1'], 'r5': ['Et0/0']}

real	0m3.108s
user	0m0.100s
sys	0m0.012s
