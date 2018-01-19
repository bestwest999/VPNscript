#include <time.h>
import paramiko
import time
import os
import datetime
config = []
with open('wonder_vpn_conf', 'r') as config_file:
        config = dict(eval(config_file.read()))

        paramiko.util.log_to_file("wonder.log");
        f = open('ASA_conf','w');
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        asa = config.setdefault('ASA_ip', None)
        client.connect(hostname= asa, port=22, username='root', password='cSc&ML&J', timeout=25)
        time.sleep(2)
        tty = client.invoke_shell()
        print(tty)
        print("Interactive SSH session established")
        time.sleep(2)
        tty.send("enable\n")
        time.sleep(2)
        tty.send("Mima&Chang\n")
        tty.send("\n")
        tty.send("copy startup-config tftp:10.44.203.161\n")
        time.sleep(2)
        tty.send("10.44.203.161\n")
        time.sleep(2)
        tty.send("ASA_conf")
        tty.send("\n")
        time.sleep(60)
        try:
            ASA_conf = open('/tftpboot/network-devices/ASA_conf', 'r')
            for line in ASA_conf:
                print(line)
        finally:
            ASA_conf.close()
        try:
            output = open('output', 'w')
            INTsubnets = dict(config.setdefault('INTsubnets', None))
            EXTsubnets = dict(config.setdefault('EXTsubnets', None))
            for i in INTsubnets.values():
                for e in EXTsubnets.values():
                    data = 'access-list TOBH line 1 extended permit ip {} {} \n'.format(i, e)
                    output.write(data)

        finally:
            output.close()

        tty.send("exit\n")


exit()