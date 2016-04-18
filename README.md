# NSXBuild
NSX automation build environment. 

This is a NSX build script created to make the following environment..

[NSX Environment](https://github.com/burnyd/NSXBuild/blob/master/nsxauto2.PNG?raw=true "NSX environment")

The assumptions are that the NSX environment is already built with controllers,clusters prepared for vibs and vteps.

The first file dlrcreation will create a Logical distributed router,logical switches and attach them to a DLR
The second file dlrrouting will create bgp peers and enable ecmp
the third file esgrouting will create 4 edge routers create bgp peerings between each esg and dlr disable edge firewall and syslog for ecmp to function properly.

All needed paramaters to make the strings work can be found within the vsphere mob.

So https://vcenterip/mob - > contenet - > rootfolder - > data center.

In the future if I need to work more with this I plan on integrating pyvnomi and netaddr or ipaddr.
