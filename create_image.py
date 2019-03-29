#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack

# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize cloud
# The URL and credentials for the 'engineering' name should be defined in the
# ~/.config/openstack/clouds.yaml or /etc/openstack/clouds.yaml.
cloud = openstack.connect(cloud='engineering')


image_name ='apappas_refhost_image'
file_name = '/home/akpappas/openstack/SLES12-SP4-JeOS.x86_64-12.4-OpenStack-Cloud-GM-clone.qcow2'
cloud_image = cloud.get_image(image_name);
image_deleted = False;
if cloud_image is None:
    cloud_image = cloud.create_image(image_name, filename = file_name,disk_format='qcow2')
else:
    # This is smelly and will be removed!
    image_deleted = cloud.delete_image(image_name, wait=True)
if image_deleted == True:
    print('Image deleted.')
else:
    print ('Image uploaded')
    
     
                           
