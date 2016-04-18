import base64
import urllib2
import httplib
import xml.etree.ElementTree as ET


global switches
global vwires
global headers
global svc_edge_id
global svc_edge_id_2
global svc_edge_id_3
global svc_edge_id_4

nsx_ip="10.0.3.15"
nsx_port = 443
username = "admin"
password = "secretpassword"
vdn_scope = 'universalvdnscope' #VNScope where all the logical swithces live
edge_datastore ='datastore-35' #Data store in which the NSX Edge routers live for 2 NSX edge routers
edge_datastore2 ='datastore-36'#Dat store in which the NSX routers lives for 2 other NSX edge routers
edge_cluster = 'domain-c32'#Edge cluster to put the ESG's inside
resource_pool ='homecluster'#Name of the cluster
datacenter_id =  'datacenter-2' #Data center where this is installed
edge_syslog = '10.2.17.190'
edge_syslog_2 = '10.26.25.9'
svc_edge_name1 = 'ESG-1' #Name of the ESG
svc_edge_name2 = 'ESG-2' #Name of ESG2
svc_edge_name3 = 'ESG-3' #Names of ESG3
svc_edge_name4 = 'ESG-4' #Names of ESG4
svc_edge_uplink_dvpg = 'dvportgroup-67' #DVportgroup for VLAN 1085 on the A side
svc_edge_uplink_dvpgb = 'dvportgroup-68' #DVportgroup for VLAN 1086 on the B side
svc_edge_uplink_dvpgc = 'universalwire-18' #VXLAN interface that connects the LDR-ESG
svc_edge_uplink_int_ip = '10.0.10.16'#ip for edge router 1 for A side
svc_edge_uplink_int_ip_b = '10.0.10.140'#ip for edge router 2 for B side
svc_edge_uplink_int_ip_c = '192.168.254.3' #ip for ESG-LDR connection
svc_edge_uplink_int_ip_2 = '10.0.10.17'
svc_edge_uplink_int_ip_b_2 = '10.0.10.141'
svc_edge_uplink_int_ip_c_2 = '192.168.254.4'
svc_edge_uplink_int_ip_3 = '10.0.10.18'
svc_edge_uplink_int_ip_b_3 = '10.0.10.142'
svc_edge_uplink_int_ip_c_3 = '192.168.254.5'
svc_edge_uplink_int_ip_4 = '10.0.10.19'
svc_edge_uplink_int_ip_b_4 = '10.0.10.143'
svc_edge_uplink_int_ip_c_4 = '192.168.254.6'
svc_edge_uplink_int_mask = '255.255.255.128'
svc_edge_as = '65001' #AS number of the ESG's
svc_switch_as = '65413' #AS number of the two top of rack switches
vdr_as = '65000' #AS number of the LDR
vdr_bgp_peer = '192.168.254.2' #IP address of the protocol address of the BGP peer from ESG - > DLR 
svc_switch_a_bgp_peer = '10.0.10.1' #IP address of the switch VLAN 1085
svc_switch_b_bgp_peer = '10.0.10.129' #IP address of the switch VLAN 1086
creds= base64.urlsafe_b64encode(username + ':' + password)
headers = {'Content-Type' : 'application/xml','Authorization' : 'Basic ' + creds }


#Creates the Edge router 1-4
def create_svc_edge(svc_edge_name,int_ip,int_ip_b,int_ip_c,int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c):
    xml_string ='<edge><datacenterMoid>'+datacenter_id+'</datacenterMoid><name>'+svc_edge_name+'</name><appliances><applianceSize>xlarge</applianceSize><appliance><resourcePoolId>'+edge_cluster+'</resourcePoolId><datastoreId>'+edge_datastore+'</datastoreId></appliance></appliances><vnics><vnic><index>'+edge_gw_int+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpg+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_b+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgb+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_b+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_c+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgc+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_c+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic></vnics></edge>'
    # Needed to use httplib to get getheader method bc NSX returning the Edge ID as a URI value in a Response Header.
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('POST', 'https://' + nsx_ip + '/api/4.0/edges',xml_string,headers)
    response = conn.getresponse()
    location = response.getheader('location', default=None)
    if response.status != 201:
            print str(response.status) + " Services Edge Not created..."
            exit(1)
    else:
            location = response.getheader('location', default=None)
            split = location.split('/')
            svc_edge_id = split[-1]
            print "Services Edge " + str(svc_edge_id)+ " Created Successfully"
            return svc_edge_id

def create_svc_edge2(svc_edge_name,int_ip,int_ip_b,int_ip_c,int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c):
    xml_string ='<edge><datacenterMoid>'+datacenter_id+'</datacenterMoid><name>'+svc_edge_name2+'</name><appliances><applianceSize>xlarge</applianceSize><appliance><resourcePoolId>'+edge_cluster+'</resourcePoolId><datastoreId>'+edge_datastore+'</datastoreId></appliance></appliances><vnics><vnic><index>'+edge_gw_int+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpg+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_2+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_b+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgb+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_b_2+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_c+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgc+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_c_2+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic></vnics></edge>'
    # Needed to use httplib to get getheader method bc NSX returning the Edge ID as a URI value in a Response Header.
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('POST', 'https://' + nsx_ip + '/api/4.0/edges',xml_string,headers)
    response = conn.getresponse()
    location = response.getheader('location', default=None)
    if response.status != 201:
            print str(response.status) + " Services Edge Not created..."
            exit(1)
    else:
            location = response.getheader('location', default=None)
            split = location.split('/')
            svc_edge_id_2 = split[-1]
            print "Services Edge " + str(svc_edge_id_2)+ " Created Successfully"
            return svc_edge_id_2


def create_svc_edge3(svc_edge_name,int_ip,int_ip_b,int_ip_c,int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c):
    xml_string ='<edge><datacenterMoid>'+datacenter_id+'</datacenterMoid><name>'+svc_edge_name3+'</name><appliances><applianceSize>xlarge</applianceSize><appliance><resourcePoolId>'+edge_cluster+'</resourcePoolId><datastoreId>'+edge_datastore+'</datastoreId></appliance></appliances><vnics><vnic><index>'+edge_gw_int+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpg+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_3+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_b+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgb+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_b_3+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_c+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgc+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_c_3+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic></vnics></edge>'
    # Needed to use httplib to get getheader method bc NSX returning the Edge ID as a URI value in a Response Header.
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('POST', 'https://' + nsx_ip + '/api/4.0/edges',xml_string,headers)
    response = conn.getresponse()
    location = response.getheader('location', default=None)
    if response.status != 201:
            print str(response.status) + " Services Edge Not created..."
            exit(1)
    else:
            location = response.getheader('location', default=None)
            split = location.split('/')
            svc_edge_id_3 = split[-1]
            print "Services Edge " + str(svc_edge_id_3)+ " Created Successfully"
            return svc_edge_id_3

def create_svc_edge4(svc_edge_name,int_ip,int_ip_b,int_ip_c,int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c):
    xml_string ='<edge><datacenterMoid>'+datacenter_id+'</datacenterMoid><name>'+svc_edge_name4+'</name><appliances><applianceSize>xlarge</applianceSize><appliance><resourcePoolId>'+edge_cluster+'</resourcePoolId><datastoreId>'+edge_datastore+'</datastoreId></appliance></appliances><vnics><vnic><index>'+edge_gw_int+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpg+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_4+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_b+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgb+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_b_4+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic><vnic><index>'+edge_gw_int_c+'</index><type>'+int_type+'</type><isConnected>true</isConnected><portgroupId>'+svc_edge_uplink_dvpgc+'</portgroupId><addressGroups><addressGroup><primaryAddress>'+svc_edge_uplink_int_ip_c_4+'</primaryAddress><subnetMask>'+int_mask+'</subnetMask></addressGroup></addressGroups><mtu>9000</mtu></vnic></vnics></edge>'
    # Needed to use httplib to get getheader method bc NSX returning the Edge ID as a URI value in a Response Header.
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('POST', 'https://' + nsx_ip + '/api/4.0/edges',xml_string,headers)
    response = conn.getresponse()
    location = response.getheader('location', default=None)
    if response.status != 201:
            print str(response.status) + " Services Edge Not created..."
            exit(1)
    else:
            location = response.getheader('location', default=None)
            split = location.split('/')
            svc_edge_id_4 = split[-1]
            print "Services Edge " + str(svc_edge_id_4)+ " Created Successfully"
            return svc_edge_id_4


#Configutes routing.  Make sure to put in the edge-id of each please!
def config_edge(svc_edge_id,edge_gw_int):
    xml_string = '<routing><routingGlobalConfig><ecmp>true</ecmp><routerId>'+svc_edge_uplink_int_ip+'</routerId><logging><enable>true</enable><logLevel>info</logLevel></logging></routingGlobalConfig><bgp><enabled>true</enabled><localAS>'+svc_edge_as+'</localAS><bgpNeighbours><bgpNeighbour><ipAddress>'+vdr_bgp_peer+'</ipAddress><remoteAS>'+vdr_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_a_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_b_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour></bgpNeighbours><redistribution><enabled>true</enabled><rules><rule><id>0</id><from><isis>false</isis><ospf>false</ospf><bgp>false</bgp><static>true</static><connected>true</connected></from><action>permit</action></rule></rules></redistribution></bgp></routing>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id + '/routing/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Routing NOT configured on SVC Edge " + str(svc_edge_id)
            exit(1)
    else:
            print str(response.status) + " Routing configured on SVC Edge " + str(svc_edge_id)
            return


def config_edge2(svc_edge_id_2,edge_gw_int):
    xml_string = '<routing><routingGlobalConfig><ecmp>true</ecmp><routerId>'+svc_edge_uplink_int_ip_2+'</routerId><logging><enable>true</enable><logLevel>info</logLevel></logging></routingGlobalConfig><bgp><enabled>true</enabled><localAS>'+svc_edge_as+'</localAS><bgpNeighbours><bgpNeighbour><ipAddress>'+vdr_bgp_peer+'</ipAddress><remoteAS>'+vdr_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_a_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_b_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour></bgpNeighbours><redistribution><enabled>true</enabled><rules><rule><id>0</id><from><isis>false</isis><ospf>false</ospf><bgp>false</bgp><static>true</static><connected>true</connected></from><action>permit</action></rule></rules></redistribution></bgp></routing>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_2 + '/routing/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Routing NOT configured on SVC Edge " + str(svc_edge_id_2)
            exit(1)
    else:
            print str(response.status) + " Routing configured on SVC Edge " + str(svc_edge_id_2)
            return

def config_edge3(svc_edge_id_3,edge_gw_int):
    xml_string = '<routing><routingGlobalConfig><ecmp>true</ecmp><routerId>'+svc_edge_uplink_int_ip_3+'</routerId><logging><enable>true</enable><logLevel>info</logLevel></logging></routingGlobalConfig><bgp><enabled>true</enabled><localAS>'+svc_edge_as+'</localAS><bgpNeighbours><bgpNeighbour><ipAddress>'+vdr_bgp_peer+'</ipAddress><remoteAS>'+vdr_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_a_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_b_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour></bgpNeighbours><redistribution><enabled>true</enabled><rules><rule><id>0</id><from><isis>false</isis><ospf>false</ospf><bgp>false</bgp><static>true</static><connected>true</connected></from><action>permit</action></rule></rules></redistribution></bgp></routing>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_3 + '/routing/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Routing NOT configured on SVC Edge " + str(svc_edge_id_3)
            exit(1)
    else:
            print str(response.status) + " Routing configured on SVC Edge " + str(svc_edge_id_3)
            return

def config_edge4(svc_edge_id_4,edge_gw_int):
    xml_string = '<routing><routingGlobalConfig><ecmp>true</ecmp><routerId>'+svc_edge_uplink_int_ip_4+'</routerId><logging><enable>true</enable><logLevel>info</logLevel></logging></routingGlobalConfig><bgp><enabled>true</enabled><localAS>'+svc_edge_as+'</localAS><bgpNeighbours><bgpNeighbour><ipAddress>'+vdr_bgp_peer+'</ipAddress><remoteAS>'+vdr_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_a_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>'+svc_switch_b_bgp_peer+'</ipAddress><remoteAS>'+svc_switch_as+'</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour></bgpNeighbours><redistribution><enabled>true</enabled><rules><rule><id>0</id><from><isis>false</isis><ospf>false</ospf><bgp>false</bgp><static>true</static><connected>true</connected></from><action>permit</action></rule></rules></redistribution></bgp></routing>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_4 + '/routing/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Routing NOT configured on SVC Edge " + str(svc_edge_id_4)
            exit(1)
    else:
            print str(response.status) + " Routing configured on SVC Edge " + str(svc_edge_id_4)
            return

#Configures Syslog on each edge
def config_syslog(svc_edge_id):
    xml_string = '<syslog><protocol>udp</protocol><serverAddresses><ipAddress>'+edge_syslog+'</ipAddress><ipAddress>'+edge_syslog_2+'</ipAddress></serverAddresses></syslog>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id +'/syslog/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Syslog not Configured on " + str(svc_edge_id)
            exit(1)
    else:
            print str(response.status) + " Syslog Configured on " + str(svc_edge_id)
            return

def config_syslog2(svc_edge_id_2):
    xml_string = '<syslog><protocol>udp</protocol><serverAddresses><ipAddress>'+edge_syslog+'</ipAddress><ipAddress>'+edge_syslog_2+'</ipAddress></serverAddresses></syslog>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_2 + '/syslog/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Syslog not Configured on " + str(svc_edge_id_2)
            exit(1)
    else:
            print str(response.status) + " Syslog Configured on " + str(svc_edge_id_2)
            return

def config_syslog3(svc_edge_id_3):
    xml_string = '<syslog><protocol>udp</protocol><serverAddresses><ipAddress>'+edge_syslog+'</ipAddress><ipAddress>'+edge_syslog_2+'</ipAddress></serverAddresses></syslog>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_3 + '/syslog/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Syslog not Configured on " + str(svc_edge_id_3)
            exit(1)
    else:
            print str(response.status) + " Syslog Configured on " + str(svc_edge_id_3)
            return

def config_syslog4(svc_edge_id_4):
    xml_string = '<syslog><protocol>udp</protocol><serverAddresses><ipAddress>'+edge_syslog+'</ipAddress><ipAddress>'+edge_syslog_2+'</ipAddress></serverAddresses></syslog>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_4 + '/syslog/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Syslog not Configured on " + str(svc_edge_id_4)
            exit(1)
    else:
            print str(response.status) + " Syslog Configured on " + str(svc_edge_id_4)
            return

#disable's firewall on each edge.  Make sure to add edge-ids
def disable_fw(svc_edge_id):
    xml_string = '<firewall><enabled>false</enabled></firewall>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id +'/firewall/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Firewall not Removed on " + str(svc_edge_id)
            exit(1)
    else:
            print str(response.status) + " Firewall removed on " + str(svc_edge_id)
            return


def disable_fw2(svc_edge_id_2):
    xml_string = '<firewall><enabled>false</enabled></firewall>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_2 + '/firewall/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Firewall not Removed on " + str(svc_edge_id_2)
            exit(1)
    else:
            print str(response.status) + " Firewall removed on " + str(svc_edge_id_2)
            return


def disable_fw3(svc_edge_id_3):
    xml_string = '<firewall><enabled>false</enabled></firewall>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_3 + '/firewall/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Firewall not Removed on " + str(svc_edge_id_3)
            exit(1)
    else:
            print str(response.status) + " Firewall removed on " + str(svc_edge_id_3)
            return


def disable_fw4(svc_edge_id_4):
    xml_string = '<firewall><enabled>false</enabled></firewall>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ svc_edge_id_4 + '/firewall/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Firewall not Removed on " + str(svc_edge_id_4)
            exit(1)
    else:
            print str(response.status) + " Firewall removed on " + str(svc_edge_id_4)
            return

def main():
    # Create a Services Edge
    int_type = 'uplink'
    edge_gw_int = '0'
    edge_gw_int_b = '1'
    edge_gw_int_c = '2'
    svc_edge_id = create_svc_edge(svc_edge_name1,svc_edge_uplink_dvpg,svc_edge_uplink_dvpgb,svc_edge_uplink_dvpgc,svc_edge_uplink_int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c)
    svc_edge_id_2 = create_svc_edge2(svc_edge_name2,svc_edge_uplink_dvpg,svc_edge_uplink_dvpgb,svc_edge_uplink_dvpgc,svc_edge_uplink_int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c)
    svc_edge_id_3 = create_svc_edge3(svc_edge_name3,svc_edge_uplink_dvpg,svc_edge_uplink_dvpgb,svc_edge_uplink_dvpgc,svc_edge_uplink_int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c)
    svc_edge_id_4 = create_svc_edge4(svc_edge_name4,svc_edge_uplink_dvpg,svc_edge_uplink_dvpgb,svc_edge_uplink_dvpgc,svc_edge_uplink_int_mask,int_type,edge_gw_int,edge_gw_int_b,edge_gw_int_c)
    #Configures routing , ecmp  
    config_edge(svc_edge_id,edge_gw_int)
    config_edge2(svc_edge_id_2,edge_gw_int)
    config_edge3(svc_edge_id_3,edge_gw_int)
    config_edge4(svc_edge_id_4,edge_gw_int)
    #Configures syslog 
    config_syslog(svc_edge_id)
    config_syslog2(svc_edge_id_2)
    config_syslog3(svc_edge_id_3)
    config_syslog4(svc_edge_id_4)
    #Disables firewall functions
    disable_fw(svc_edge_id)
    disable_fw2(svc_edge_id_2)
    disable_fw3(svc_edge_id_3)
    disable_fw4(svc_edge_id_4)
    print " \n Created the Edge routers \n"
main()


