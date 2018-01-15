#include <time.h>
import paramiko
import time
import os
import datetime
config = []
with open('wonder_vpn_conf', 'r') as config_file:
    config = dict(eval(config_file.read()))

        paramiko.util.log_to_file("filename.log");
        f = open('ASA_conf','w');
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname= config.setdefault('ASA_ip', None), port=22, username='test', password='test', timeout=25)
        time.sleep(2)
        tty = client.invoke_shell()
        print(tty)
        print("Interactive SSH session established")
        time.sleep(2)
        tty.send("enable\n")
        time.sleep(2)
        tty.send("test\n")
        tty.send("\n")
        time.sleep(2)
        tty.send("copy startup-config tftp:10.44.203.161\n")
        time.sleep(2)
        tty.send("10.44.203.161\n")
        time.sleep(2)
        b = datetime.date.today().strftime("%B %d %Y")
        a = ip
        c = a+b
        d = c.replace(" ","_")
        tty.send(d)
        tty.send("\n")
        time.sleep(60)
        output = tty.recv(10000)
        print(output)
tty.send("exit\n")




try:
    output = open('output', 'w')
    INTsubnets = dict(config.setdefault('INTsubnets', None))
    EXTsubnets = dict(config.setdefault('EXTsubnets', None))
    for i in INTsubnets.values():
        for e in EXTsubnets.values():
            data = 'access-list TOBH line 1 extended permit ip {} {} \n'.format(i, e )
            output.write(data)

finally:
    output.close()
exit()