#!/usr/bin/env python3
# -*- coic.ding: utf-8 -*-
"""
Created on Thu May 21 11:12:54 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import glob, os
from astropy.io import fits
from tqdm import trange

import init_cfg as ic


# ----- Coadding images ----- #
for i in np.arange(len(ic.filters)):
	for j in np.arange(len(ic.tracts)):

		### Making single extension images
		calexp_list = glob.glob(ic.dir_coadd+ic.filters[i]+'/'+ic.tracts[j]+'/*/calexp*.fits')
		calexp_list = sorted(calexp_list)
		print('Dividing extensions of ['+ic.filters[i]+'/'+ic.tracts[j]+'] images')
		for k in trange(len(calexp_list)):
			img, hd1 = fits.getdata(calexp_list[k], ext=1, header=True)
			var, hd3 = fits.getdata(calexp_list[k], ext=3, header=True)

			imgname = calexp_list[k].split('/')[-1]
			num_patch = imgname.split('-')[-1].split('.fits')[0]
			num_patch = num_patch.replace(',', 'x')

			fits.writeto(ic.filters[i]+ic.tracts[j]+'-'+num_patch+'.fits',
		                 img, hd1, overwrite=True)
			fits.writeto(ic.filters[i]+ic.tracts[j]+'-'+num_patch+'.var.fits',
		                 var, hd3, overwrite=True)

		### Writing & running the SWarp command
		os.system('swarp -dd > config.swarp')
		comm = 'swarp '
		for k in np.arange(len(calexp_list)):
			imgname = calexp_list[k].split('/')[-1]
			num_patch = imgname.split('-')[-1].split('.fits')[0]
			num_patch = num_patch.replace(',', 'x')
			comm += ic.filters[i]+ic.tracts[j]+'-'+num_patch+'.fits '
		newimg = ic.fields[j]+'-'+ic.filters[i].split('-')[1]
		comm += '-c config.swarp '

		comm1 = comm+'-IMAGEOUT_NAME '+newimg+'.fits -WEIGHTOUT_NAME '+newimg+'.weight.fits '
		comm1 += f"-SUBTRACT_BACK N -PIXELSCALE_TYPE MANUAL -PIXEL_SCALE {ic.pixscale:.3f} "
		comm1 += f"-SATLEV_DEFAULT {ic.upper_limit:.1f} "
		comm1 += '-CENTER_TYPE MANUAL -CENTER '+ic.ra0[j]+','+ic.dec0[j]+f" -IMAGE_SIZE {int(ic.isize):d} "
		print(comm1)
		os.system(comm1)

		comm2 = comm+'-IMAGEOUT_NAME b'+newimg+'.fits -WEIGHTOUT_NAME b'+newimg+'.weight.fits '
		comm2 += f"-SUBTRACT_BACK Y -PIXELSCALE_TYPE MANUAL -PIXEL_SCALE {ic.pixscale:.3f} "
		comm2 += f"-SATLEV_DEFAULT {ic.upper_limit:.1f} -BACK_SIZE {ic.BACKS_swp:d} "
		comm2 += '-CENTER_TYPE MANUAL -CENTER '+ic.ra0[j]+','+ic.dec0[j]+f" -IMAGE_SIZE {int(ic.isize):d} "
		print(comm2)
		os.system(comm2)

		os.system('rm -rf '+ic.filters[i]+ic.tracts[j]+'-*.fits')


if (glob.glob("Images/") == []):
	os.system("mkdir Images")
else:
	os.system("rm -rfv Images/*")
os.system("mv -v *.fits Images/")


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
