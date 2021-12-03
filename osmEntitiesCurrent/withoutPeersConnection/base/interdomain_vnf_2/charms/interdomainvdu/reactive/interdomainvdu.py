import glob
import json
from charms.reactive import (
    hook,
    clear_flag,
    when,
    when_not,
    set_flag
)

import charms.sshproxy
from charmhelpers.core import hookenv, unitdata
from charmhelpers.core.hookenv import (
    application_version_set,
    config,
    log,
    status_set,
    function_fail,
    function_set,
    function_get
)

config=config()
db=unitdata.kv()

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

        cmd = ['sudo apt install {} -y'.format("net-tools")]    
        result, err = charms.sshproxy._run(cmd)
        set_flag('interdomainvdu.apt.installed')
        status_set('maintenance', 'Package Wireguard Installed')
    except:
        log('command failed:' + err)
        set_flag('interdomainvdu.apt.not_installed')
        status_set('error', 'Unable to install packages')


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
        set_flag('config.keygen')


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
            log(x+":"+result)
        except:
            log('command failed:' + err)
            log('cat '+x+' failed')
            set_flag('keygen.failed')
        
    set_flag('keygen.done')
    log("Key Generation done")
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
        set_flag('interdomainvdu.load.keys.failed')
    finally:
        key=result
  
    conf="/etc/wireguard/"+config['forward_interface']+".conf"

    wg_conf="[Interface]\nAddress = "+config['tunnel_address']+"\nSaveConfig = "+str(config['save_config'])+"\nListenPort = "+str(config['listen_port'])+"\nPrivateKey = "+key+"\n\n"

    log(wg_conf)

    result=err = ''
    try:
        cmd = ['echo "{}" |sudo tee {}'.format(wg_conf,conf)]
        result, err = charms.sshproxy._run(cmd)
        log(result)
        set_flag('wireguard.start')
    except:
        log('command failed:' + err)
        set_flag('wireguard.server.config.failed')
    

@when('wireguard.start')
@when_not('interdomainvdu.installed')
def start_wireguard():
    status_set('maintenance','Wireguard quick start')
    result=err = ''
    try:
        forward_interface=config['forward_interface']
        
        cmd = ['sudo wg-quick up {}'.format(forward_interface)]
        result, err = charms.sshproxy._run(cmd)
        log(result)
    except:
        log('command failed:' + err)
        set_flag('wireguard.server.start.failed')

    log("Wireguard interface up:\n"+result)
    
    result=err = ''
    try:
        cmd = ['sudo wg show {}'.format(config['forward_interface'])]
        result, err = charms.sshproxy._run(cmd)
        log(result)
    except:
        log('command failed:' + err)
        set_flag('wireguard.server.config.failed')

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
        filename = function_get('filename')
        cmd = ['touch {}'.format(filename)]
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        clear_flag('actions.touch')

##############

@when('actions.addpeer')
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
        #peer_key= function_get('peer_key')
        #peer_endpoint = function_get('peer_endpoint')
        peer_network= function_get('peer_network')
  
        conf="/etc/wireguard/"+config['forward_interface']+".conf"
        wgconf="\n\n[Peer]\nPublicKey = <peer_key>\nEndpoint = <peer_endpoint>:<listen_port>\nAllowedIPs = "+peer_network+"\n\n"
        # """
        # [Peer]
        # PublicKey= peer_key
        # Endpoint = peer_endpoint
        # AllowedIPs = peer_network
        # """

        cmd = ['echo "{}" | sudo tee -a {}'.format(wgconf,conf)]
        log(cmd)
        result, err = charms.sshproxy._run(cmd)
    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)
    
    # Don't try to to set the WG interface
    #try:           
    #    cmd = ['sudo wg-quick up {}'.format(config['forward_interface'])]
    #    result, err = charms.sshproxy._run(cmd)
    #except:
    #    function_fail('command failed:' + err)
    #    log('command failed:' + err)
    #else:
    #    function_set({'output': result, "errors": err})
    #finally:
    #    log(result)

    clear_flag('actions.addpeer')

##############

@when('actions.getvnfinfo')
@when('interdomainvdu.installed')
def getVnfIp():
    result=err = ''

    try:
        vnfMgmtIp = config['ssh-hostname']
        tunnelAddress = config['tunnel_address']
        tunnelId = config['tunnel_id']
        vsiId = config['vsi_id']

        bandwidth = config['bandwidth']

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
            cmd = ['sudo ip addr 2>/dev/null | echo $(awk "/^[0-9]+: [a-z]/ { sub(\\":\\",\\"\\") ; sub(\\":\\",\\"\\") ; iface = \$2 ; getline ; print \\"\\\\\\"\\"iface\\"\\\\\\":\\",\\"\\\\\\"\\"\$2\\"\\\\\\",\\" }"| grep -v 00:00:00:00:00:00) | awk "{print \\"{\\"substr(\$0, 1, length(\$0)-1)\\"}\\"}"']
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.getinterfacesmacs.failed')
        finally:
            log("interfacesMACs: "+result)
            interfacesAndMACs=json.loads(result)

        try:
            cmd = ['sudo arp -n 2>/dev/null | grep "^$(sudo route -n 2>/dev/null | grep ^0.0.0.0 | awk "{print \$2}" | head -n 1) " | awk "{print \$3}"']
            result, err = charms.sshproxy._run(cmd)
        except:
            log('command failed:' + err)
        else:
            set_flag('interdomainvdu.getgwmac.failed')
        finally:
            log("gwMAC: "+result)
            gwMAC=result

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

        vnfMgmtIp=vnfMgmtIp.split("/")[0]
        
        interfacesAndIps=list(interfacesAndIps.items())

        log("using interface: "+str(interfacesAndIps[0])+" with MAC "+interfacesAndMACs[interfacesAndIps[0][0]])

        result=json.dumps({"vsiId":vsiId,"publicKey": publicKey,"vnfIp":vnfMgmtIp, "tunnelId":tunnelId, "vnfMAC":interfacesAndMACs[interfacesAndIps[0][0]], "gwMAC":gwMAC})

    except:
        function_fail('command failed:' + err)
    else:
        function_set({'output': result, "errors": err})
    finally:
        log(result)

    clear_flag('actions.getvnfinfo')