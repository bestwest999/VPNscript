import paramiko
import time
import os
import datetime
import re
config = []
map = [] # route-map number

def tunnel(key, peer):         # function for generating tunnel-group conf
    tunnel1 = 'tunnel-group {} type ipsec-l2l\n'.format(peer)
    tunnel2 = 'tunnel-group {} ipsec-attributes\n'.format(peer)
    tunnel3 = 'ikev1 pre-shared-key {}\n'.format(key)
    output.writelines(tunnel1)
    output.writelines(tunnel2)
    output.writelines(tunnel3)
    output.writelines('isakmp keepalive threshold 10 retry 3\nexit\n')

# currect asa conf checking for free crypto map number
with open('ASA_conf', 'r') as ASA:
    for line in ASA:
        if re.match('crypto map NEW [1-9]', line):
            line = line.split()
            map.append(line[3])
    map = int(max(map)) + 1

with open('wonder_vpn_conf', 'r') as config_file:
        config = dict(eval(config_file.read()))
        try:
            output = open('output', 'w')

            # main variables
            CryptoMap = config.setdefault('crypto_map', None)
            ACL_name = config.setdefault('ACL_name', None)
            Transform_name = config.setdefault('transform_set_name', None)
            key = config.setdefault('KEY', None)
            pfs = config.setdefault('PFS', None)
            no_natOBJ = config.setdefault('NOVPN_NETWOR_OBJECT', None)

            # Route map and tunnel configuration
            REMOTE_peer = dict(config.setdefault('REMOTE_peer', None))
            if (len(REMOTE_peer)>1):
                peers = []
                for i in REMOTE_peer.values():
                    tunnel(key, i)
                    peers.append(i) # remote peers list
                routemap1 = 'crypto map {} {} set peer {} {} \n'.format(CryptoMap, map, peers[0], peers[1])
                output.writelines(routemap1)
            else:
                peer = REMOTE_peer.setdefault('peer', None)
                tunnel(key, peer)
                routemap1 = 'crypto map {} {} set peer {}\n'.format(CryptoMap, map, peer)
                output.writelines(routemap1)

            routemap2 = 'crypto map {} {} match address {}\n'.format(CryptoMap, map, ACL_name)
            routemap3 = 'crypto map {} {} set ikev1 transform-set {}\n'.format(CryptoMap, map, Transform_name)
            output.writelines(routemap2)
            output.writelines(routemap3)

            # PFS conf
            if (pfs == 'yes'):
                pfs = 'crypto map ADSTREAM {} set pfs\n'.format(map)
                output.writelines(pfs)

            # access-list configuration
            INTsubnets = dict(config.setdefault('INTsubnets', None))
            EXTsubnets = dict(config.setdefault('EXTsubnets', None))
            asa = config.setdefault('ASA_ip', None)
            print(asa)
            for i in INTsubnets.values():
                for e in EXTsubnets.values():
                    data = 'access-list {} line 1 extended permit ip {} {} \n'.format(ACL_name, i, e)
                    output.write(data)
            # NAT configuration
            nat_obj1 = 'object-group network {}\n'.format(no_natOBJ)
            output.writelines(nat_obj1)
            for e in EXTsubnets.values():
                nat_obj = 'network-object {}\n'.format(e)
                output.writelines(nat_obj)
            output.writelines('object-group network VPN_NONAT\n')
            nat_obj2 = 'group-object {}'.format(no_natOBJ)
            output.writelines(nat_obj2)


        finally:
            output.close()

        exit()