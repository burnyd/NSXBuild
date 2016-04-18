""" Future to do's
Import Netaddr and figure out a better way to create IP addresses/bgp neighbors
Import Pyvnmoni and figure out a way to create distributed port groups on a dvs
Add Getters at some point in pyvnmoni to figure out everything that is found in the vsphere mob.
"""

import base64
import urllib2
import httplib
import xml.etree.ElementTree as ET


global switches
global vwires
global headers

#Most of the information needed to make the strings work can be found within the vsphere MOB https://vcenterip/MOB - > Content - > root folder.
nsx_ip="10.0.3.15" #NSX manager ip or dns name
nsx_port = 443 #NSX manager port
username = "admin" #NSX manager username
password = "supersecretpassword" #NSX manager API password
vdn_scope = 'universalvdnscope' #transport zone
edge_datastore ='datastore-35'# data store where the ldr will reside
edge_cluster = 'domain-c32' #cluster where the ldr will be installed
resource_pool ='homecluster'#name of the cluster where the ldr will be installed
vdr_edge_name = 'Test-Universal-DLR' #Name of the ldr
vdr_mgmt_pg = 'dvportgroup-73'#distributed port group needed for the ldr 
vdr_mgmt_pg_name ='VTEP-902'#port group name for the management of the ldr
internal_ls_names = ['Web-10.0.100.0/24','APP-10.0.101.0/24','DB-10.0.102.0/24'] #List of logical switches
transport_ls_name = 'transport-LDR-ESG-192.168.254.0/25' #Name of the LDR to ESG logical switch name
datacenter_id =  'datacenter-2' #vsphere mob data center id
datacenter_name = 'home' #vsphere data center name
vdr_as = "65000" #bgp AS of the LDR
vdr_protocol_address = '192.168.254.2' #Protocol address for the source of bgp
vdr_forwarding_address = '192.168.254.1'#Forwarding address for BGP to use
bgp_neighbor = '192.168.254.3' #ESG neighbor 1
bgp_neighbor_2 = '192.168.254.4' #ESG neighbor 2
bgp_neighbor_3 = '192.168.254.5' #ESG neighbor 3
bgp_neighbor_4 = '192.168.265.6' #ESg neighbor 4
svc_edge_as = '65001' #ESG BGP AS number

creds= base64.urlsafe_b64encode(username + ':' + password)
headers = {'Content-Type' : 'application/xml','Authorization' : 'Basic ' + creds }

#Creates each of the logical switches.  This is using Hybrid mode this can be changed within the API call.  Same goes with the description. 
def create_ls(ls_name):
    url='https://' + nsx_ip + '/api/2.0/vdn/scopes/'+vdn_scope+'/virtualwires'
    xml_string ='<virtualWireCreateSpec><name>' + ls_name + '</name><description>dlr created python script</description><tenantId>virtual wire tenant</tenantId><controlPlaneMode>HYBRID_MODE</controlPlaneMode></virtualWireCreateSpec>'
    req = urllib2.Request(url=url,data=xml_string,headers=headers)
    response=urllib2.urlopen(req)
    vwire_id=response.read()
    return vwire_id


#Creates the LDR/VDR
def create_vdr(edge_name):
    xml_string ='<edge><datacenterMoid>'+datacenter_id+'</datacenterMoid><datacenterName>'+datacenter_name+'</datacenterName><tenant>default</tenant><name>'+vdr_edge_name+'</name><enableAesni>true</enableAesni><enableFips>false</enableFips><vseLogLevel>info</vseLogLevel><appliances><applianceSize>compact</applianceSize><appliance> <highAvailabilityIndex>0</highAvailabilityIndex><resourcePoolId>'+edge_cluster+'</resourcePoolId><resourcePoolName>'+resource_pool+'</resourcePoolName><datastoreId>'+edge_datastore+'</datastoreId><vmFolderId>group-v3</vmFolderId><vmFolderName>vm</vmFolderName><deployed>true</deployed></appliance><appliance><highAvailabilityIndex>1</highAvailabilityIndex><resourcePoolId>'+edge_cluster+'</resourcePoolId><resourcePoolName>'+resource_pool+'</resourcePoolName><datastoreId>'+edge_datastore+'</datastoreId><vmFolderName>vm</vmFolderName><deployed>true</deployed></appliance><deployAppliances>true</deployAppliances></appliances><cliSettings><remoteAccess>true</remoteAccess><userName>admin</userName><password>VMware12345678!</password><sshLoginBannerText>***************************************************************************PNC UniversaDLR****************************************************************************</sshLoginBannerText><passwordExpiry>99999</passwordExpiry></cliSettings><features><featureConfig/><firewall><version>1</version><enabled>false</enabled><defaultPolicy><action>deny</action><loggingEnabled>false</loggingEnabled></defaultPolicy><firewallRules><firewallRule><id>131075</id><ruleTag>131075</ruleTag><name>dns</name><ruleType>internal_high</ruleType><enabled>true</enabled><loggingEnabled>false</loggingEnabled><description>dns</description><action>accept</action><source><exclude>false</exclude><vnicGroupId>internal</vnicGroupId></source><destination><exclude>false</exclude><ipAddress>1.1.1.1</ipAddress></destination><application><service><protocol>udp</protocol><port>53</port><sourcePort>any</sourcePort></service><service><protocol>tcp</protocol><port>53</port><sourcePort>any</sourcePort></service></application></firewallRule></firewallRules></firewall></features><autoConfiguration><enabled>true</enabled><rulePriority>high</rulePriority></autoConfiguration><type>distributedRouter</type><isUniversal>true</isUniversal><hypervisorAssist>false</hypervisorAssist><queryDaemon><enabled>false</enabled><port>5666</port></queryDaemon><mgmtInterface><label>vNic_0</label><name>mgmtInterface</name><addressGroups/><mtu>1500</mtu><index>0</index><connectedToId>'+vdr_mgmt_pg+'</connectedToId><connectedToName>'+vdr_mgmt_pg_name+'</connectedToName></mgmtInterface><localEgressEnabled>false</localEgressEnabled></edge>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('POST', 'https://' + nsx_ip + '/api/4.0/edges',xml_string,headers)
    response = conn.getresponse()
    location = response.getheader('location', default=None)
    if response.status != 201:
            print str(response.status) +" VDR Not created..."
            exit(1)
    else:
            location = response.getheader('location', default=None)
            split = location.split('/')
            edge_id = split[-1]
            print "VDR " + str(edge_id)+' Created Successfully'
            return edge_id

#Connects each of the logical switches to their respective VDR
def connect_ls(edge_id,vwire_name,vwire_id,int_ip,int_mask,int_type):
    print str(vwire_id) +' : ' + str(int_ip) + ' : ' + str(int_type)
    url='https://' + nsx_ip + '/api/4.0/edges/' + edge_id + '/interfaces/?action=patch'
    xml_string ='<interfaces><interface><name>' + vwire_name + '</name><addressGroups><addressGroup><primaryAddress>' + int_ip + '</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu><type>' + int_type + '</type><isConnected>true</isConnected><connectedToId>' + vwire_id + '</connectedToId></interface></interfaces>'
    req = urllib2.Request(url=url,data=xml_string,headers=headers)
    response=urllib2.urlopen(req)

def main():
    vwires = []
    print " Creating Logical Switches..."
    for i in internal_ls_names: #For loop to loop every list entry configured in internal_ls_names up top.
        vwire_id = create_ls(i)
        vwires.append(vwire_id)
    print "----The following Logical Switches were created:  " + str(vwires)

  # Create a VDR
    print " Creating Distributed Logical Router... "
    vdr_edge_id = create_vdr(vdr_edge_name)

   # Create the LDR-ESG connection
    print "Creating and configuring Transport LS Interface on " + str(vdr_edge_id) + ' Distributed Logical Router'
    int_ip = '192.168.254.1'
    int_mask ='255.255.255.128'
    int_type = 'uplink'
    transport_vwire_id = create_ls(transport_ls_name)
    print "Transport vwire_id String = " + str(transport_vwire_id)
    lif_name=transport_vwire_id + '-API'
    uplk_lif = connect_ls(vdr_edge_id,lif_name,transport_vwire_id,int_ip,int_mask,int_type)
    print "Done. PLEASE MANUALLY ENABLE HA AS THERE IS NO WAY TO ENABLE IT WITH UNIVERSAL DLR. Transport LS Interface configured on " + str(vdr_edge_id)

# Create LIFS on VDR create above
    # X variable is the begining of the third octet string so for example if you are starting at 10.1.240.0/24 makes x 240
    x=100
    print " Creating and configuring VDR Interfaces or LIFs..."
    for index, ls_id in enumerate(vwires):
        xstring = str(x)
        x+= 1 # Add's a 1 to the string concatination
        int_ip = '10.0.' + xstring + '.1' #starts with 10.1.(x) then adds a string of .1 at the very end to the layer 3 interface.
        int_mask='255.255.255.0'
        int_type = 'internal'
        name = ls_id +'-API'
        int_lif = connect_ls(vdr_edge_id,name,ls_id,int_ip,int_mask,int_type)

main()

