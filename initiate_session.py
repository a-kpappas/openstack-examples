#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def initiate_session(path=""):
    from keystoneauth1 import loading
    from keystoneauth1 import session
    import yaml
    import os
   
    if path=="":
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
    return sess