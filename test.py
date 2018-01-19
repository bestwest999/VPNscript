import paramiko
import time
import os
import datetime
import re
config = []
map = [] # route-map number
with open('wonder_vpn_conf', 'r') as config_file:
        config = dict(eval(config_file.read()))
        try:
            output = open('output', 'w')
            INTsubnets = dict(config.setdefault('INTsubnets', None))
            EXTsubnets = dict(config.setdefault('EXTsubnets', None))
            asa = config.setdefault('ASA_ip', None)
            print(asa)
            for i in INTsubnets.values():
                for e in EXTsubnets.values():
                    data = 'access-list TOBH line 1 extended permit ip {} {} \n'.format(i, e)
                    output.write(data)
            with open('ASA_conf', 'r') as ASA:

                for line in ASA:
                    if re.match('crypto map NEW [1-9]', line):
                        line = line.split()
                        map.append(line[3])
                print(max(map))



        finally:
            output.close()

        exit()