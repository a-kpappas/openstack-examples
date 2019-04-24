#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:48:58 2019

@author: akpappas
"""
import os
import guestfs
import wget
import subprocess

from shutil import copy

image_name = 'SLES12-SP4-JeOS.x86_64-12.4-OpenStack-Cloud-GM.qcow2';
if not os.path.isfile(image_name):
    url = 'http://download.suse.de/install/SLE-12-SP4-JeOS-GM/'+image_name;
    image_name = wget.download(url);
original_image = image_name;
image_name = image_name + 'edited';
copy(original_image, image_name);


authorized_keys = os.path.abspath('authorized_keys');
if os.path.isfile(authorized_keys):
    os.remove(authorized_keys);
wget.download('http://qam.suse.de/downloads/authorized_keys',
              out=authorized_keys);
             

g = guestfs.GuestFS(python_return_dict=True);
g.add_drive(image_name);
g.launch();
g.mount('/dev/sda3','/');
g.download('/etc/cloud/cloud.cfg','cloud.cfg');
subprocess.call("sed 's/^disable_root:[^:]\+/disable_root: false/' cloud.cfg > cloud.cfg.new",shell=True);
g.upload('cloud.cfg.new', '/etc/cloud/cloud.cfg');
try:
    g.mkdir('/root/.ssh/');
except RuntimeError as e:    
    if e.args[0].find('File exists') > 0 :
        g.rm_rf('/root/.ssh/')
        g.mkdir('/root/.ssh/');
    else:
        print('Unrecoverable error.');
        print(e.args[0]);
        raise       
g.chmod(0o700,'/root/.ssh');
g.upload(authorized_keys,'/root/.ssh/authorized_keys');
g.chmod(0o600,'/root/.ssh/authorized_keys');
g.close();
    
