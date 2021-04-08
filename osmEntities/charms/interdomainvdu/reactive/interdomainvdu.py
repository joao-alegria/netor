import glob
import json
import subprocess as sp
#from charms import apt
from charms.reactive import (
    hook,
    clear_flag,
    when,
    when_not,
    set_flag
)

import charms.sshproxy
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import (
    application_version_set,
    config,
    log,
    status_set,
    action_get,
    function_fail,
    function_set
)
from charmhelpers.fetch import get_upstream_version

# sudo ethtool -s ens3 speed 100 duplex full autoneg off

# ifconfig | echo $(awk '/^[a-z]/ { sub(":",""); iface = $1; getline; sub("addr:", ""); print "\""iface"\":","\""$2"\"," }' | grep -v 127.0.0.1) | awk '{print "{"substr($0, 1, length($0)-1)"}"}'

config=config()

@when('sshproxy.configured')
@when_not('interdomainvdu.installed')
def install_packages():
    status_set('maintenance', 'Installing wireguard')
    result=err = ''
    try:
        package="wireguard"
        cmd = ['sudo apt update']
        result, err = charms.sshproxy._run(cmd)
        log("updated packages")
        cmd = ['sudo apt install {} -y'.format(package)]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('interdomainvdu.apt.not_installed')
    finally:
        set_flag('interdomainvdu.apt.installed')
        status_set('maintenance', 'Package Wireguard Installed')

@when('interdomainvdu.apt.installed')
@when_not('interdomainvdu.installed')
def wireguard_version_check():
    log('setting application version')
    
    result=err = ''
    
    try: 
        cmd = ['wg --version']
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
        log('wireguard not installed')
    finally:
        status_set('maintenance', result)
        
        # files=glob.glob("files/*key")
        # count=0

        # if not config['wg_server']:
        #     set_flag('config.keygen')
        # else:
        #     for x in files:
        #         with open(x) as f:
        #             if f.read() is not None:
        #                 count+=1        
        #         f.close()
        #     if count==2:
        set_flag('config.keygen')
        # else:
        #     set_flag('config.loadkey')

@when('config.keygen')
@when_not('interdomainvdu.installed')
def configuration_keygen():
    status_set('maintenance', 'Wireguard Key generation')
        
    private_key_path="/etc/wireguard/privatekey"
    public_key_path="/etc/wireguard/publickey"
    key_location=[private_key_path,public_key_path]
 
    log('Key Generation start')
    result=err = ''
    
    try:
        
        cmd = ['wg genkey | sudo tee {} | wg pubkey | sudo tee {}'.format(key_location[0],key_location[1])]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('keygen.failed')
    finally:
        set_flag('keygen.done')
        status_set('maintenance', 'Keygen Done')
    
        status_set('maintenance',result)
    
    for x in key_location:
        result=err = ''
        try:
            cmd = ['sudo cat {}'.format(x)]
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
            log('cat '+x+' failed')
        else:
            set_flag('keygen.failed')
        finally:
            log(x+":"+result)
        
    set_flag('keygen.done')
    log("Key Generation done")
    # if config['wg_server']: 
    #     set_flag('interdomainvdu.server.config')
    # else:
    set_flag('interdomainvdu.tunnel.config')

@when('config.loadkey')
@when_not('interdomainvdu.installed')
def configuration_loadkey():
    status_set('maintenance', 'Wireguard Load Keys')

    private_key_path="/etc/wireguard/privatekey"
    public_key_path="/etc/wireguard/publickey"
    key_location=[private_key_path,public_key_path]
    
    for x in key_location:
        key=""
        y="files/"+x.lstrip('/etc/wireguard/')
        
        with open(y,'r') as f:
            key=f.read()
        f.close()
        result=err = ''
        try:
            cmd = ['echo {} |sudo tee {}'.format(key,x)]
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.load.keys.failed')
        finally:
            key=result
    status_set('maintenance', 'Load Keys')
    set_flag('interdomainvdu.tunnel.config')

@when('interdomainvdu.tunnel.config')
@when_not('interdomainvdu.installed')
def wireguard_server_configuration():
    status_set('maintenance', 'Server wireguard configuration started')
    result=err = ''
    try:
        filename="/etc/wireguard/privatekey"
        cmd = ['sudo cat {}'.format(filename)]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('interdomainvdu.load.keys.failed')
    finally:
        key=result
  
    conf="/etc/wireguard/"+config['forward_interface']+".conf"

    wg_conf="[Interface]\nAddress = "+config['tunnel_address']+"\nSaveConfig = "+str(config['save_config'])+"\nListenPort = "+str(config['listen_port'])+"\nPrivateKey = "+key+"\n\n"

    # \nPostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o "+config['forward_interface']+" -j MASQUERADE"+"\nPostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o "+config['forward_interface']+" -j MASQUERADE

    # """[Interface]
    # Address = server_tunnel_address
    # SaveConfig = save_config
    # ListenPort = listen_port
    # PrivateKey = key
    # PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o forward_interface -j MASQUERADE
    # PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o forward_interface -j MASQUERADE"""

    log(wg_conf)

    result=err = ''
    try:
        cmd = ['echo "{}" |sudo tee {}'.format(wg_conf,conf)]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('wireguard.server.config.failed')
    finally:
        log(result)
        set_flag('wireguard.start')
    

# @when('interdomainvdu.client.config')
# @when_not('interdomainvdu.installed')
# def wireguard_client_configuration():
#     status_set('maintenance', 'Client wireguard configuration started')
    
#     result=err = ''
#     try:
#         filename="/etc/wireguard/privatekey"
#         cmd = ['sudo cat {}'.format(filename)]
#         result, err = charms.sshproxy._run(cmd)
#     except:
#         log('command failed:' + err)
#     else:
#         set_flag('interdomainvdu.load.keys.failed')
#     finally:
#         clientprivatekey=result
    
#     with open("files/privatekey",'r') as f:
#         serverkey=f.read()
#     f.close()
    
#     with open("files/publickey",'r') as f:
#         serverpubkey=f.read()
#     f.close()
    

#     ##TODO Save server public key in the client machine

#     conf="/etc/wireguard/"+config['forward_interface']+".conf"

#     wg_conf="[Interface]\nPrivateKey= "+clientprivatekey+"\nAddress = "+config['client_tunnel_address']+"\nListenPort = "+str(config['listen_port'])+"\n\n[Peer]\nPublicKey= "+serverpubkey+"\nEndpoint = "+config['server_public_address'].split('/')[0]+":"+str(config['listen_port'])+"\nAllowedIPs = 0.0.0.0/0"

#     """[Interface]
#     PrivateKey= clientprivatekey
#     Address = client_tunnel_address
#     ListenPort = listen_port
    
#     [Peer]
#     PublicKey= serverpubkey
#     Endpoint = server_public_address
#     AllowedIPs = 0.0.0.0/0"""
    
#     log(wg_conf)

#     result=err = ''
#     try:
#         cmd = ['echo "{}" |sudo tee {}'.format(wg_conf,conf)]
#         result, err = charms.sshproxy._run(cmd)
#     except:
#         log('command failed:' + err)
#     else:
#         set_flag('wireguard.server.config.failed')
#     finally:
#         log(result)
#         set_flag('wireguard.start')

@when('wireguard.start')
@when_not('interdomainvdu.installed')
def start_wireguard():
    # if not config['wg_server']:
    #     status_set('active','Wireguard Client installed and configured')
    #     set_flag('interdomainvdu.installed')

    # else:
    status_set('maintenance','Wireguard quick start')
    result=err = ''
    try:
        forward_interface=config['forward_interface']
        
        cmd = ['sudo wg-quick up {}'.format(forward_interface)]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('wireguard.server.start.failed')
    finally:
        log(result)

    log("Wireguard interface up:\n"+result)
    
    result=err = ''
    try:
        cmd = ['sudo wg show {}'.format(config['forward_interface'])]
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + err)
    else:
        set_flag('wireguard.server.config.failed')
    finally:
        log(result)

    # log("IM HERE!!!!!!!!")

    result=err = ''
    try:
        cmd = ['sudo dhclient']
        result, err = charms.sshproxy._run(cmd)
    except:
        log('command failed:' + result)
        log('command failed:' + err)
    else:
        set_flag('wireguard.server.config.failed')
    finally:
        log(result)
    
    log("Wireguard config:\n"+result)
    status_set('active','Wireguard installed and configured')
    set_flag('interdomainvdu.installed')
    status_set('active', 'Ready!')

#
##Actions
#

@when('actions.touch')
@when('interdomainvdu.installed')
def touch():
    result=err = ''
    try:
        filename = action_get('filename')
        cmd = ['touch {}'.format(filename)]
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        clear_flag('actions.touch')

##############

# @when('actions.confclient')
# @when('interdomainvdu.client.config')
# @when('interdomainvdu.installed')
# def configure_client():
#     status_set('maintenance', 'Client wireguard configuration started')
    
#     result=err = ''
#     try:
#         filename="/etc/wireguard/privatekey"
#         cmd = ['sudo cat {}'.format(filename)]
#         result, err = charms.sshproxy._run(cmd)
#     except:
#         log('command failed:' + err)
#     else:
#         set_flag('interdomainvdu.load.keys.failed')
#     finally:
#         clientprivatekey=result
    
#     serverpubkey=action_get('server_public_key')
#     server_public_address=action_get('server_public_address')
#     log(type(serverpubkey))
#     log(type(server_public_address))
#     log(server_public_address.split('/')[0])

#     conf="/etc/wireguard/"+config['forward_interface']+".conf"

#     wg_conf="[Interface]\nPrivateKey= "+clientprivatekey+"\nAddress = "+config['client_tunnel_address']+"\nListenPort = "+str(config['listen_port'])+"\n\n[Peer]\nPublicKey= "+serverpubkey+"\nEndpoint = "+server_public_address.split('/')[0]+":"+str(config['listen_port'])+"\nAllowedIPs = 0.0.0.0/0"

#     """
#     [Interface]
#     PrivateKey= clientprivatekey
#     Address = client_tunnel_address
#     ListenPort = listen_port
    
#     [Peer]
#     PublicKey= serverpubkey
#     Endpoint = server_public_address
#     AllowedIPs = 0.0.0.0/0
#     """
    
#     log(wg_conf)

#     result=err = ''
#     try:
#         cmd = ['echo "{}" |sudo tee {}'.format(wg_conf,conf)]
#         result, err = charms.sshproxy._run(cmd)
#     except:
#         function_fail('command failed:' + err)
#     else:
#         function_set({'output': result, "errors": err})
#     finally:
#         set_flag('tunnel.configured')
#         clear_flag('actions.confclient')

####

# @when('actions.connserver')
# @when('tunnel.configured')
# @when('interdomainvdu.installed')
# def connect_server():
#     result=err = ''
#     if not action_get('confirmation'):
#         function_fail('command failed; confirmation needed')
#     else:
#         status_set('maintenance','Wireguard client quick start')
#         result=err = ''
#         try:           
#             cmd = ['sudo wg-quick up {}'.format(config['forward_interface'])]
#             result, err = charms.sshproxy._run(cmd)
#         except:
#             function_fail('command failed:' + err)
#             log('command failed:' + err)
#         else:
#             function_set({'output': result, "errors": err})
#             set_flag('wireguard.server.start.failed')
#         finally:
#             log(result)

#         log("Wireguard interface up:\n"+result)
       
#         result=err = ''
#         try:
#             cmd = ['sudo wg show {}'.format(config['forward_interface'])]
#             result, err = charms.sshproxy._run(cmd)
#         except:
#             function_fail('command failed:' + err)
#             log('command failed:' + err)
#         else:
#             function_set({'output': result, "errors": err})
#             set_flag('wireguard.server.config.failed')
#         finally:
#             log(result)
#             clear_flag('actions.connserver')

#         log("Wireguard config:\n"+result)
#         status_set('active','Wireguard installed and configured')

#         status_set('active', 'Tunnel Ready!')

####

@when('actions.addpeer')
# @when('interdomainvdu.server.config')
@when('interdomainvdu.installed')
def addpeer():
    result=err = ''

    try:           
        cmd = ['sudo wg-quick down {}'.format(config['forward_interface'])]
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
        log('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)

    result=err = ''

    try:
        peer_key= action_get('peer_key')
        peer_endpoint = action_get('peer_endpoint')
        peer_network= action_get('peer_network')
  
        conf="/etc/wireguard/"+config['forward_interface']+".conf"
        wgconf="\n\n[Peer]\nPublicKey= "+peer_key+"\nEndpoint = "+peer_endpoint+":"+str(config['listen_port'])+"\nAllowedIPs = "+peer_network+"\n\n"

        # """[Peer]
        # PublicKey= peer_key
        # Endpoint = peer_endpoint
        # AllowedIPs = peer_network"""


        cmd = ['echo "{}" | sudo tee -a {}'.format(wgconf,conf)]
        log(cmd)
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)
    
    try:           
        cmd = ['sudo wg-quick up {}'.format(config['forward_interface'])]
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
        log('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)

    clear_flag('actions.addpeer')

####

@when('actions.sendvnfinfo')
@when('interdomainvdu.installed')
def sendVnfIp():
    result=err = ''

    try:
        vnfMgmtIp = config['ssh-hostname']
        tunnelAddress = config['tunnel_address']
        tunnelId = config['tunnel_id']
        vsiId = config['vsi_id']
        vsEndpoint = action_get('vsEndpoint')

        log(config)

        try:
            cmd = ['ifconfig | echo $(awk "/^[a-z]/ { sub(\\":\\",\\"\\"); iface = \$1; getline; sub(\\"addr:\\", \\"\\"); print \\"\\\\\\"\\"iface\\"\\\\\\":\\",\\"\\\\\\"\\"\$2\\"\\\\\\",\\" }"| grep -v 127.0.0.1) | awk "{print \\"{\\"substr(\$0, 1, length(\$0)-1)\\"}\\"}"']
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.getinterfaces.failed')
        finally:
            log("interfaces: "+result)
            interfacesAndIps=json.loads(result)

        try:
            filename="/etc/wireguard/publickey"
            cmd = ['sudo cat {}'.format(filename)]
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.load.keys.failed')
        finally:
            publicKey=result

        if len(interfacesAndIps)==3:

            vnfMgmtIp=vnfMgmtIp.split("/")[0]
            tunnelAddress=tunnelAddress.split("/")[0]

            for key, value in interfacesAndIps.items():
                if value != vnfMgmtIp and value != tunnelAddress:
                    vnfIp=value
                    config["data_address"]=vnfIp
                    config["data_interface"]=key

            data={"vsiId":vsiId,"publicKey": publicKey,"vnfIp":vnfIp, "tunnelId":tunnelId}
  
            cmd = ['curl -X POST -H "Content-Type: application/json"  -d {} {}'.format(json.dumps(json.dumps(data)),vsEndpoint)]
            log(cmd)
            result, err = charms.sshproxy._run(cmd)
        else:
            log('Expecting 3 network interfaces')
            function_fail('Expecting 3 network interfaces')
    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)

    clear_flag('actions.sendvnfinfo')


@when('actions.modifytunnel')
@when('interdomainvdu.installed')
def modifyTunnel():
    result=err = ''

    try:
        try:
            bandwidth = action_get('bandwidth')
            data_interface = config['data_interface']

            if data_interface == "error":
                function_fail('the data interface was not updated')

            cmd = ['sudo ethtool -s {} speed {} duplex full autoneg off'.format(data_interface, bandwidth)]
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.getinterfaces.failed')


    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)