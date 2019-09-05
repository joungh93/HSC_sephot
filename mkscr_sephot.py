#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 20:58:50 2019

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import os
from astropy.io import fits

import init_patch as ip


# ----- Making script for all the patches ----- #
f = open('sephot_all.sh','w')
f.write(' \n')
f.write('##################################'+'\n')
f.write('##### Scripts for SExtractor #####'+'\n')
f.write('##################################'+'\n')        
f.write(' \n')
for i in np.arange(len(ip.patchstr_dir)):
    f.write('# ----- HSC patch : '+ip.patchstr_img[i]+'----- #'+'\n')
    f.write(' \n')    
    f.write('sex Comb'+ip.patchstr_sex[i]+'.fits,G'+ip.patchstr_sex[i]+'.fits -c config.sex -CATALOG_NAME G'+ip.patchstr_sex[i]+'.cat -DETECT_THRESH 2.0 -ANALYSIS_THRESH 2.0 -PHOT_APERTURES 4.0,6.0,8.0,10.0,12.0,18.0,24.0,33.3 -MAG_ZEROPOINT 27.0 -GAIN 12780.0 -SEEING_FWHM 3.8 -BACK_SIZE 32 -PSF_NAME prepsfex_g.psf'+'\n')    
    f.write('sex Comb'+ip.patchstr_sex[i]+'.fits,R'+ip.patchstr_sex[i]+'.fits -c config.sex -CATALOG_NAME R'+ip.patchstr_sex[i]+'.cat -DETECT_THRESH 2.0 -ANALYSIS_THRESH 2.0 -PHOT_APERTURES 4.0,6.0,8.0,10.0,12.0,18.0,24.0,33.3 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 3.6 -BACK_SIZE 32 -PSF_NAME prepsfex_r.psf'+'\n')    
    f.write('sex Comb'+ip.patchstr_sex[i]+'.fits,I'+ip.patchstr_sex[i]+'.fits -c config.sex -CATALOG_NAME I'+ip.patchstr_sex[i]+'.cat -DETECT_THRESH 2.0 -ANALYSIS_THRESH 2.0 -PHOT_APERTURES 4.0,6.0,8.0,10.0,12.0,18.0,24.0,33.3 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 3.9 -BACK_SIZE 32 -PSF_NAME prepsfex_i.psf'+'\n')
    f.write(' \n')     
    f.write('rm -rfv G'+ip.patchstr_sex[i]+'.fits R'+ip.patchstr_sex[i]+'.fits I'+ip.patchstr_sex[i]+'.fits'+'\n')
    f.write('rm -rfv mG'+ip.patchstr_sex[i]+'.fits mR'+ip.patchstr_sex[i]+'.fits'+'\n')
    f.write('rm -rfv ker_G'+ip.patchstr_sex[i]+'.fits')
    f.write('rm -rfv ker_R'+ip.patchstr_sex[i]+'.fits')
    f.write('rm -rfv Comb'+ip.patchstr_sex[i]+'.fits')
    f.write(' \n\n') 
f.close()

# ----- Running scripts for PSFEx ----- #
os.system('rm -rfv *.lis')
os.system('sh sephot_all.sh')  


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))

