#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#This needs to be turned in to a function with these params.
server_name = 'apappas-refhost-test';
import openstack

# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize cloud
cloud = openstack.connect(cloud='engineering')


cloud_server = cloud.get_server(server_name)

# List available floating IPs
f_ip=cloud.available_floating_ip(network='floating')
floating_ip = f_ip['floating_ip_address']
print("Available floating IP %s" % floating_ip)

# Create a floating IP in the network.
# The network ID is retrieved by the flavors_images_networks.py

netlist = cloud.network.networks();
f_identity = None;
for net in netlist:
    if net.name=='floating':
        f_identity = net.id;
    break

if f_identity is None:
    raise ValueError("Couldn't find floating ip id!");
    

f_ip = cloud.network.create_ip(floating_network_id=f_identity)
f_ip_address = f_ip.floating_ip_address
print("Created floating IP %s" % f_ip_address)


# Add the available floating IP to the server
cloud.compute.add_floating_ip_to_server(server=cloud_server,address=floating_ip)

cloud.pprint(cloud_server)

