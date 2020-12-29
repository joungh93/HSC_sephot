#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:40:26 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import glob, os
from astropy.io import fits

import init_cfg as ic


# ----- Making scripts for PSFEx ----- #
os.system("psfex -dd > config.psfex")

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
	f.write('# ----- HSC field : '+ic.fields[i]+' ----- #'+'\n')
	f.write('\n')
	for j in np.arange(len(ic.filters)):
		flt = ic.filters[j].split('-')[1]
		f.write('rm -rfv prepsfex_'+flt+'.cat\n')
		f.write('sex Images/'+prefix+ic.fields[i]+'-'+flt+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_'+flt+'.cat ')
		f.write('-DETECT_THRESH {0:.1f} -ANALYSIS_THRESH {0:.1f} '.format(ic.THRES_psf))
		f.write(f"-MAG_ZEROPOINT {ic.MAG0:.1f} -GAIN {ic.GAIN0[j]:.1f} -SEEING_FWHM {ic.SEEING0:.2f}\n")
		f.write('sex Images/'+prefix+ic.fields[i]+'-'+flt+'.fits -c prepsfex.sex -CATALOG_NAME prepsfex_'+ic.fields[i]+'-'+flt+'.cat -CATALOG_TYPE ASCII_HEAD ')
		f.write('-DETECT_THRESH {0:.1f} -ANALYSIS_THRESH {0:.1f} '.format(ic.THRES_psf))
		f.write(f"-MAG_ZEROPOINT {ic.MAG0:.1f} -GAIN {ic.GAIN0[j]:.1f} -SEEING_FWHM {ic.SEEING0:.2f}\n")
		f.write('psfex prepsfex_'+flt+'.cat -c config.psfex ')
		f.write(f"-SAMPLE_FWHMRANGE {ic.FWHMR_psf[0]:.1f},{ic.FWHMR_psf[1]:.1f} ")
		f.write(f"-SAMPLE_MINSN {ic.MINSN_psf:.1f} -SAMPLE_MAXELLIP {ic.MAXEL_psf:.2f} ")
		f.write('-OUTCAT_TYPE ASCII_HEAD -OUTCAT_NAME psf_'+ic.fields[i]+'-'+flt+'.cat ')
		f.write('-CHECKPLOT_TYPE NONE -XML_NAME psf_'+ic.fields[i]+'-'+flt+'.xml\n')
		f.write('mv -v prepsfex_'+flt+'.psf psf_'+ic.fields[i]+'-'+flt+'.psf')
		f.write('\n')
	f.write('\n\n')
f.close()


# ----- Running scripts for PSFEx ----- #
if (glob.glob("PSFEx/") == []):
	os.system("mkdir PSFEx")
else:
	os.system("rm -rfv PSFEx/*")

os.system("sh psfex_all.sh")

os.system("mv -v psf_*.cat psf_*.xml psf_*.psf PSFEx/")
os.system("mv -v prepsfex_*-*.cat PSFEx/")
os.system("rm -rfv ./*.fits prepsfex_*.cat")


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
