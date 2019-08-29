#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:13:33 2019

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import os
from astropy.io import fits

import init_patch as ip

from pyraf import iraf
iraf.images()
iraf.immatch()


# ----- Making combined images ----- #
for i in np.arange(len(ip.patchstr_dir)):
	print("Patch : "+ip.patchstr_dir[i])
	img_G = 'G'+ip.patchstr_sex[i]+'.fits'
	img_R = 'R'+ip.patchstr_sex[i]+'.fits'
	img_I = 'I'+ip.patchstr_sex[i]+'.fits'

	os.system('ls -1 '+img_G+' '+img_R+' > inp'+ip.patchstr_sex[i]+'.lis')
	f = open('ker'+ip.patchstr_sex[i]+'.lis','w')
	f.write('ker_'+img_G+'\n')
	f.write('ker_'+img_R+'\n')
	f.close()
	os.system('rm -rfv '+'Comb'+ip.patchstr_sex[i]+'.fits')
	os.system('rm -rfv '+'m'+img_G+' '+'m'+img_R)
	os.system('rm -rfv '+'ker_'+img_G+' '+'ker_'+img_R)

	try:
		iraf.psfmatch(input='@inp'+ip.patchstr_sex[i]+'.lis', referenc=img_I,
			          psfdata='psf_I'+ip.patchstr_sex[i]+'.reg', kernel='@ker'+ip.patchstr_sex[i]+'.lis',
			          output='m//@inp'+ip.patchstr_sex[i]+'.lis', convolu='image', dnx=31, dny=31, pnx=15, pny=15)

		dat_G = fits.getdata('m'+img_G)
		dat_R = fits.getdata('m'+img_R)
		dat_I = fits.getdata(img_I)

		fits.writeto('Comb'+ip.patchstr_sex[i]+'.fits', (dat_G+dat_R+dat_I)/3.0, overwrite=True)

	except:
		dat_G = fits.getdata(img_G)
		dat_R = fits.getdata(img_R)
		dat_I = fits.getdata(img_I)

		fits.writeto('Comb'+ip.patchstr_sex[i]+'.fits', (dat_G+dat_R+dat_I)/3.0, overwrite=True)


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))