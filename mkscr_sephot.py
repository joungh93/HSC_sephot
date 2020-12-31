#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:43:14 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import os
from astropy.io import fits

import init_cfg as ic


if ic.use_backsub:
    prefix = 'b'
else:
    prefix = ''


# ----- Making SExtractor photometry scripts ----- #
dir_img = "Images/"
dir_psf = "PSFEx/"
fwhm_out = np.loadtxt(dir_psf+"fwhm_out.txt")

f = open('sephot_all.sh','w')
f.write(' \n')
f.write('##################################'+'\n')
f.write('##### Scripts for SExtractor #####'+'\n')
f.write('##################################'+'\n')        
f.write(' \n')

for i in np.arange(len(ic.fields)):
    f.write('\n# ----- '+ic.fields[i]+' ----- #\n')
    for j in np.arange(len(ic.filters)):
        flt = ic.filters[j].split('-')[1]
        f.write('sex '+dir_img+'c'+prefix+ic.fields[i]+'.fits,'+dir_img+prefix+ic.fields[i]+'-'+flt+'.fits -c config.sex ')
        f.write('-CATALOG_NAME '+prefix+ic.fields[i]+'-'+flt+'.cat ')
        f.write(f"-DETECT_MINAREA {ic.MINAR_sep:d} -DETECT_THRESH {ic.THRES_sep:.1f} -ANALYSIS_THRESH {ic.THRES_sep:.1f} ")
        f.write('-FILTER_NAME '+ic.FILTR_sep+f" -DEBLEND_NTHRESH {ic.DEBLN_sep:d} -DEBLEND_MINCONT {ic.DEBLM_sep:.3f} ")
        if ic.APHOT:
            f.write('-PHOT_APERTURES '+ic.APERs+' ')
        f.write(f"-MAG_ZEROPOINT {ic.MAG0:.1f} ")
        f.write(f"-GAIN {ic.GAIN0[i][j]:.1f} -SEEING_FWHM {fwhm_out[i]*ic.pixscale:.2f} ")
        f.write(f"-BACK_SIZE {ic.BACKS_sep:d} -BACKPHOTO_TYPE LOCAL ")
        f.write('-PSF_NAME '+dir_psf+'psf_'+ic.filters[j]+'.psf\n')
f.close()


# ----- Running scripts for SExtractor ----- #
os.system('sh sephot_all.sh')


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))

