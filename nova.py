#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:17:49 2019

@author: akpappas
"""

from neutronclient.v2_0 import client as neutron_client
from keystoneauth1 import loading
from keystoneauth1 import session
import yaml
import os


if os.path.isfile("clouds.yaml"):
    path = "clouds.yaml";
elif os.path.isfile(os.path.expanduser('~/')+'.config/openstack/clouds.yaml'):
    path = os.path.expanduser('~/')+".config/openstack/clouds.yaml";
elif os.path.isfile("/etc/openstack/clouds.yaml"):
    path= "/etc/openstack/clouds.yaml";
else:
    raise Exception("clouds.yaml not found.")

with open(path,'r') as stream:
    credentials = yaml.safe_load(stream)
credentials = credentials["clouds"]["engineering"]["auth"]

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url = credentials["auth_url"],
                                username = credentials["username"],
                                password = credentials["password"],
                                project_id = credentials["project_id"],
                                user_domain_name= credentials["user_domain_name"])
sess = session.Session(auth=auth)
nova = client.Client("2",session=sess)
servers = nova.servers.list();
neutron = neutron_client.Client(session=sess)
security_groups = neutron.list_security_groups()['security_groups']





    