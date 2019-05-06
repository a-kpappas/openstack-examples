#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:17:49 2019

@author: akpappas
"""

import initiate_session
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client


sess = initiate_session.initiate_session()
nova = nova_client.Client("2",session=sess)
servers = nova.servers.list();
neutron = neutron_client.Client(session=sess)
security_groups = neutron.list_security_groups()['security_groups']





    