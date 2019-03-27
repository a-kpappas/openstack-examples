#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openstack

# Initialize and turn on debug logging
openstack.enable_logging(debug=True)

# Initialize cloud
# The URL and credentials for the 'engineering' name should be defined in the
# ~/.config/openstack/clouds.yaml or /etc/openstack/clouds.yaml.
cloud = openstack.connect(cloud='engineering')

# Create new instance
# The image and flavor is specific to the OpenStack service.
# See the flavors_and_images.py example on how to list the available 
# images and flavors
image_name='apappas_refhost_image'
cloud_image = cloud.get_image(image_name);
if cloud_image is None:
    cloud_image = cloud.create_image('apappas_refhost_image', filename ='SLES12-SP4-JeOS.x86_64-12.4-OpenStack-Cloud-GM.qcow2',disk_format='qcow')
                                     
