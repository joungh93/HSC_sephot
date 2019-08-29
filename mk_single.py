#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 09:46:35 2019

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
from astropy.io import fits

import init_patch as ip


# ----- Making single extension images ----- #
di = '/data/jlee/HSCv6/M81/Bell/Red/rerun/object/deepCoadd-results/'
filt = ['HSC-G','HSC-R','HSC-I']
for i in np.arange(len(ip.patchstr_dir)):
    for j in np.arange(len(filt)):
        print("Images : "+filt[j]+'/'+ip.patchstr_dir[i])
        dat, hdr = fits.getdata(di+filt[j]+'/'+ip.patchstr_dir[i]+'/calexp-'+filt[j]+'-'+ip.patchstr_img[i]+'.fits', extn=1, header=True)
        fits.writeto(filt[j].split('-')[1]+ip.patchstr_sex[i]+'.fits', dat, hdr, overwrite=True)


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))