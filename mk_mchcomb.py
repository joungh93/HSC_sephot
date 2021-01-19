#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:13:33 2019

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import glob, os, copy
import pandas as pd
from astropy.io import fits
from astropy.convolution import Gaussian2DKernel
from astropy.convolution import convolve

import init_cfg as ic


dir_psf = "PSFEx/"

if ic.use_backsub:
	prefix = 'b'
else:
	prefix = ''


# ----- FWHMs of images ----- #
fwhm_in = np.zeros((len(ic.fields), len(ic.filters)))
for i in np.arange(len(ic.fields)):
	print("\n----- Field : "+ic.fields[i]+" -----")
	for j in np.arange(len(ic.filters)):
		flt = ic.filters[j].split('-')[1]
		xml_psf = pd.read_csv(dir_psf+"xml_psf_"+flt+f"-{i:d}.csv")
		fwhm_in[i,j] = xml_psf['FWHM_Mean'].values[0]
		print(ic.filters[j]+f" mean PSF FWHM : {fwhm_in[i,j]:.3f} pix")
fwhm_out = np.max(fwhm_in, axis=1)
j_ref = np.argmax(fwhm_in, axis=1)

sigma_in = fwhm_in / np.sqrt(8.*np.log(2.))
sigma_out = fwhm_out / np.sqrt(8.*np.log(2.))
np.savetxt(dir_psf+"fwhm_out.txt", fwhm_out, fmt="%.4f")


# ----- Combining PSF-matched images ----- #
for i in np.arange(len(ic.fields)):
	flt0 = ic.filters[0].split('-')[1]
	img = fits.getdata("Images/"+prefix+ic.fields[i]+"-"+flt0+".fits")
	cimg = np.zeros((img.shape[0], img.shape[1], len(ic.filters)))
	out = "c"+prefix+ic.fields[i]+".fits"
	print("\nWriting "+out+" ...")
	for j in np.arange(len(ic.filters)):
		flt = ic.filters[j].split('-')[1]
		img, hdr = fits.getdata("Images/"+prefix+ic.fields[i]+"-"+flt+".fits",
			                    header=True)
		if (j == j_ref[i]):
			cimg[:,:,j] = img
		else:
			sigma_kernel = np.sqrt(sigma_out[i]**2.0 - sigma_in[i,j]**2.0)
			kernel = Gaussian2DKernel(x_stddev=sigma_kernel, y_stddev=sigma_kernel)
			img_conv = convolve(img, kernel)
			cimg[:,:,j] = img_conv
		cimg2 = np.median(cimg, axis=2)
		hdr['BITPIX'] = -32
		fits.writeto("Images/"+out, cimg2, hdr, overwrite=True)
	print("---> Reference filter: "+ic.filters[j_ref[i]])


# Printing the running time  
print("\n--- %s seconds ---" % (time.time() - start_time))
