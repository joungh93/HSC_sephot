#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:40:26 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import os
from astropy.io import fits

import init_cfg as ic


# ----- Making scripts for PSFEx ----- #
if ic.use_backsub:
	prefix = 'b'
else:
	prefix = ''

f = open('psfex_all.sh','w')
f.write('\n')
f.write('#############################'+'\n')
f.write('##### Scripts for PSFEx #####'+'\n')
f.write('#############################'+'\n')
f.write('\n')
for i in np.arange(len(ic.fields)):
	f.write('# ----- HSC field : '+ic.fields[i]+'----- #'+'\n')
	f.write('\n')
	for j in np.arange(len(ic.filters)):
		flt = ic.filters[j].split('-')[1]
		f.write('sex Images/'+prefix+ic.fields[i]+'-'+flt+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_'+flt+'.cat ')
		f.write('-DETECT_THRESH {0:.1f} -ANALYSIS_THRESH {0:.1f} '.format(ic.THRES_psf))
		f.write(f"-MAG_ZEROPOINT {ic.MAG0:.1f} -GAIN {ic.GAIN0[j]:.1f} -SEEING_FWHM {ic.SEEING0:.2f}\n")
		f.write('sex Images/'+prefix+ic.fields[i]+'-'+flt+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_'+ic.fields[i]+'-'+flt+'.cat -CATALOG_TYPE ASCII_HEAD ')
		f.write('-DETECT_THRESH {0:.1f} -ANALYSIS_THRESH {0:.1f} '.format(ic.THRES_psf))
		f.write(f"-MAG_ZEROPOINT {ic.MAG0:.1f} -GAIN {ic.GAIN0[j]:.1f} -SEEING_FWHM {ic.SEEING0:.2f}\n")
		f.write('psfex prepsfex_'+flt+'.cat -c config.psfex ')
		f.write(f"-SAMPLE_FWHMRANGE {ic.FWHMR_psf[0]:.1f},{ic.FWHMR_psf[1]:.1f} ")
		f.write(f"-SAMPLE_MINSN {ic.MINSN_psf:.1f} -SAMPLE_MAXELLIP {ic.MAXEL_psf:.2f} ")
		f.write('-OUTCAT_NAME psf_'+ic.fields[i]+'-'+flt+'.cat\n')
		f.write('\n')
	f.write('\n\n')

f.close()


# ----- Running scripts for PSFEx ----- #
os.system('sh psfex_all.sh')    


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
