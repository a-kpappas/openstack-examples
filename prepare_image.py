#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def prepare_image(image_name=""):
    import os
    import guestfs
    import wget
    import subprocess
    import shutil
    if image_name == "":
        print("No image name provided")
        image_name='SLES12-SP4-JeOS.x86_64-12.4-OpenStack-Cloud-GM.qcow2'
        print("Defaulting to "+image_name)
    if not os.path.isfile(image_name):
        url = 'http://download.suse.de/install/SLE-12-SP4-JeOS-GM/'+image_name;
        print("JeOS image not available locally.")
        print("Downloading "+url+"...");
        image_name = wget.download(url);
    
    new_image = 'edited.qcow2';
    if os.path.isfile(new_image):
        print("Deleting previously edited image.")
        print("To avoid that rename it from 'edited.qcow2' before running this tool")
        os.remove(new_image);

    shutil.copy(image_name, new_image);
    del image_name;
    #Downloading ssh keys of the QAM keys so that they can connect to the
    #refhost we will create
    authorized_keys = os.path.abspath('authorized_keys');
    if os.path.isfile(authorized_keys):
        os.remove(authorized_keys);
    print("Downloading ssh keys.");
    wget.download('http://qam.suse.de/downloads/authorized_keys',
                  out=authorized_keys);
                 
    #Edited the default openstack jeos image to add the root user and add the
    #QAM keys to their authorized keys.
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
            raise;   
    g.chmod(0o700,'/root/.ssh');
    g.upload(authorized_keys,'/root/.ssh/authorized_keys');
    g.chmod(0o600,'/root/.ssh/authorized_keys');
    g.close();
    os.remove('cloud.cfg');
    os.remove('cloud.cfg.new');    
    return os.path.abspath(new_image)
