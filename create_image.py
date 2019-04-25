#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack
import os
# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize cloud
# The URL and credentials for the 'engineering' name should be defined in the
# ~/.config/openstack/clouds.yaml or /etc/openstack/clouds.yaml.

image_name ='apappas_refhost_image'
file_name = 'edited.qcow2'
if not os.path.isfile(file_name):
    print("No image to upload. Exiting.");
    exit();

cloud = openstack.connect(cloud='engineering')
cloud_image = cloud.get_image(image_name);

if cloud_image is None:
    print("Image doesn't exist in the cloud");
else:
    print("Deleting existing image");
    cloud.delete_image(image_name, wait=True);

print("Uploading new image.");
cloud_image = cloud.create_image(image_name, 
                                 filename=file_name, 
                                 disk_format='qcow2');

    
     
                           
