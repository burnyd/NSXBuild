import base64
import urllib2
import httplib
import xml.etree.ElementTree as ET

nsx_ip="10.0.3.15"
nsx_port = 443
username = "admin"
password = "supersecretpassword"
vdr_as = "6500"
vdr_protocol_address = '192.168.254.2'
vdr_forwarding_address = '192.168.254.1'
bgp_neighbor = '192.168.254.3'
bgp_neighbor_2 = '192.168.254.4'
bgp_neighbor_3 = '192.168.254.5'
bgp_neighbor_4 = '192.168.254.6'
svc_edge_as = '65001'
vdr_edge_id = 'edge-c5ffe29d-4c62-4a93-9fc6-0b888bfe8fcd'

creds= base64.urlsafe_b64encode(username + ':' + password)
headers = {'Content-Type' : 'application/xml','Authorization' : 'Basic ' + creds }

def config_vdr():
    xml_string = '<routing><routingGlobalConfig><ecmp>true</ecmp><routerId>' + vdr_forwarding_address + '</routerId><logging><enable>true</enable><logLevel>info</logLevel></logging></routingGlobalConfig><bgp><enabled>true</enabled><localAS>' + vdr_as + '</localAS><bgpNeighbours><bgpNeighbour><ipAddress>' + bgp_neighbor + '</ipAddress><protocolAddress>' + vdr_protocol_address + '</protocolAddress><forwardingAddress>' + vdr_forwarding_address + '</forwardingAddress><remoteAS>' + svc_edge_as + '</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>' + bgp_neighbor_2 + '</ipAddress><protocolAddress>' + vdr_protocol_address + '</protocolAddress><forwardingAddress>' + vdr_forwarding_address + '</forwardingAddress><remoteAS>' + svc_edge_as + '</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>' + bgp_neighbor_3 + '</ipAddress><protocolAddress>' + vdr_protocol_address + '</protocolAddress><forwardingAddress>' + vdr_forwarding_address + '</forwardingAddress><remoteAS>' + svc_edge_as + '</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour><bgpNeighbour><ipAddress>' + bgp_neighbor_4 + '</ipAddress><protocolAddress>' + vdr_protocol_address + '</protocolAddress><forwardingAddress>' + vdr_forwarding_address + '</forwardingAddress><remoteAS>' + svc_edge_as + '</remoteAS><weight>60</weight><holdDownTimer>3</holdDownTimer><keepAliveTimer>1</keepAliveTimer></bgpNeighbour></bgpNeighbours><redistribution><enabled>true</enabled><rules><rule><id>0</id><from><isis>false</isis><ospf>false</ospf><bgp>false</bgp><static>true</static><connected>true</connected></from><action>permit</action></rule></rules></redistribution></bgp></routing>'
    conn = httplib.HTTPSConnection(nsx_ip, nsx_port)
    conn.request('PUT', 'https://' + nsx_ip + '/api/4.0/edges/'+ vdr_edge_id +'/routing/config',xml_string,headers)
    response = conn.getresponse()
    if response.status != 204:
            print str(response.status) + " Routing NOT configured on SVC Edge " + str(vdr_edge_id)
            exit(1)
    else:
            print str(response.status) + " Routing configured on SVC Edge " + str(vdr_edge_id)
            return

def main():

#Configures the routing ie ECMP and BGP to peer with the 4 BGP neighbors from the DLR
        config_vdr()

main()

