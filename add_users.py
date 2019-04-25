#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import guestfs
import wget
import subprocess
import shutil

original_image='SLES12-SP4-JeOS.x86_64-12.4-OpenStack-Cloud-GM.qcow2'
if not os.path.isfile(original_image):
    print("No JeOS image available.")
    url = 'http://download.suse.de/install/SLE-12-SP4-JeOS-GM/'+original_image;
    print("Downloading "+url);
    original_image = wget.download(url);

new_image = 'edited.qcow2';
if os.path.isfile(new_image):
    os.remove(new_image);
shutil.copy(original_image, new_image);


authorized_keys = os.path.abspath('authorized_keys');
if os.path.isfile(authorized_keys):
    os.remove(authorized_keys);

print("Downloading ssh keys");
wget.download('http://qam.suse.de/downloads/authorized_keys',
              out=authorized_keys);
             

g = guestfs.GuestFS(python_return_dict=True);
g.add_drive(new_image);
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

os.remove('cloud.cfg');
os.remove('cloud.cfg.new');    
