#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 09:46:55 2019

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import os
from astropy.io import fits

import init_patch as ip


# ----- Making scripts for PSFEx ----- #
f = open('psfex_all.sh','w')
f.write('\n')
f.write('#############################'+'\n')
f.write('##### Scripts for PSFEx #####'+'\n')
f.write('#############################'+'\n')
f.write('\n')
for i in np.arange(len(ip.patchstr_dir)):
	f.write('# ----- HSC patch : '+ip.patchstr_img[i]+'----- #'+'\n')
	f.write('\n')
	f.write('sex G'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_g.cat -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 12780.0 -SEEING_FWHM 4.10'+'\n')
	f.write('sex G'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_G'+ip.patchstr_sex[i]+'.cat -CATALOG_TYPE ASCII_HEAD -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 12780.0 -SEEING_FWHM 4.10'+'\n')
	f.write('psfex prepsfex_g.cat -c config.psfex -SAMPLE_FWHMRANGE 3.0,5.0 -SAMPLE_MINSN 5.0 -SAMPLE_MAXELLIP 0.18 -OUTCAT_NAME psf_G'+ip.patchstr_sex[i]+'.cat'+'\n')
	f.write('\n')
	f.write('sex R'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_r.cat -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 4.00'+'\n')
	f.write('sex R'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_R'+ip.patchstr_sex[i]+'.cat -CATALOG_TYPE ASCII_HEAD -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 4.00'+'\n')
	f.write('psfex prepsfex_r.cat -c config.psfex -SAMPLE_FWHMRANGE 3.0,5.0 -SAMPLE_MINSN 5.0 -SAMPLE_MAXELLIP 0.18 -OUTCAT_NAME psf_R'+ip.patchstr_sex[i]+'.cat'+'\n')
	f.write('\n')
	f.write('sex I'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_i.cat -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 4.40'+'\n')
	f.write('sex I'+ip.patchstr_sex[i]+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_I'+ip.patchstr_sex[i]+'.cat -CATALOG_TYPE ASCII_HEAD -DETECT_THRESH 10.0 -ANALYSIS_THRESH 10.0 -MAG_ZEROPOINT 27.0 -GAIN 10080.0 -SEEING_FWHM 4.40'+'\n')
	f.write('psfex prepsfex_i.cat -c config.psfex -SAMPLE_FWHMRANGE 3.0,5.0 -SAMPLE_MINSN 5.0 -SAMPLE_MAXELLIP 0.18 -OUTCAT_NAME psf_I'+ip.patchstr_sex[i]+'.cat'+'\n')
	f.write('\n\n')
f.close()


# ----- Running scripts for PSFEx ----- #
os.system('sh psfex_all.sh')    


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))