#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:17:49 2019

@author: akpappas
"""

import initiate_session
import prepare_image
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client
from glanceclient import client as glance_client
import openstack


sess = initiate_session.initiate_session("")
openstack.enable_logging(debug=True)
conn = openstack.connect(cloud='engineering')    
nova = nova_client.Client("2",session=sess,http_log_debug=True)
glance = glance_client.Client('2', session=sess)


image_path = prepare_image.prepare_image()
image_name = "apappas_image"
#Check if image exists
cloud_image = conn.get_image(image_name)
#If it does, delete it.
if cloud_image is not None:
    print("Deleting existing image")
    conn.delete_image(image_name, wait = True)

#Upload image.
cloud_image = conn.create_image(image_name, 
                                 filename=image_path, 
                                 disk_format='qcow2')

#Check if server exists
server_name = "apappas-refhost-test"
server = conn.compute.find_server(server_name)
if server is not None:
    conn.compute.delete_server(server)


#Find the groups that will allow communtication to the VM
sg_allow_all = conn.network.find_security_group("allow-all")
sg_all_open = conn.network.find_security_group("all_open")
sg_list = [sg_all_open, sg_allow_all]

server = conn.create_server(name = server_name,
                          image = image_name,
                          flavor=dict(id='22'),
                          wait=True,
                          auto_ip=True)



netlist = conn.network.networks();
f_identity = None;
for net in netlist:
    if net.name=='floating':
        f_identity = net.id;
    break

if f_identity is None:
    raise ValueError("Couldn't find floating ip id!");
    

f_ip = conn.network.create_ip(floating_network_id=f_identity)
f_ip_address = f_ip.floating_ip_address
print("Created floating IP %s" % f_ip_address)


# Add the available floating IP to the server
conn.compute.add_floating_ip_to_server(server=server,address=f_ip_address)
conn.compute.add_security_group_to_server(server=server,security_group=sg_all_open)
conn.compute.add_security_group_to_server(server=server,security_group=sg_allow_all)