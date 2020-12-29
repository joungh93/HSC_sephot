#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:30:41 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import pandas as pd
import init_cfg as ic

colname = ['ID', 'fwhm_sep', 'flxrad_sep', 'ell_sep', 'fwhm_psf', 'ell_psf']
dir_psf = "PSFEx/"

for i in np.arange(len(ic.fields)):
	for j in np.arange(len(ic.filters)):
		
		print("Reading PSFEx data of "+ic.fields[i]+" ("+ic.filters[j]+") ...")

		flt = ic.filters[j].split('-')[1]
		data_psf = np.genfromtxt(dir_psf+'psf_'+ic.fields[i]+'-'+flt+'.cat', dtype=None,
                                 encoding='ascii', usecols=(0,3,6,7,11,12,13,14,15),
                                 names=('num','flag','x','y','fwhm','ell','snr','chi2','resi'))
		
		# PSF-selected sources
		sel = (data_psf['flag'] == 0)
		n_psfsel = np.sum(sel)

		# Writing a region file of PSF-selected sources
		f = open(dir_psf+'psf_'+ic.fields[i]+'-'+flt+'.reg','w')
		for k in np.arange(n_psfsel):
			f.write(f"{data_psf['x'][sel][k]:.3f}  {data_psf['y'][sel][k]:.3f}"+'\n')
		f.close()

		# Reading a SExtractor catalog
		prepsf = np.genfromtxt(dir_psf+'prepsfex_'+ic.fields[i]+'-'+flt+'.cat', dtype=None,
		                       encoding='ascii', usecols=(1600,1601,1604,1605,1606),
		                       names=('x','y','flxrad','fwhm','ell'))

		d_prepsf = pd.DataFrame(data = {colname[0] : data_psf['num'][sel],
			                            colname[1] : prepsf['fwhm'][sel],
		                                colname[2] : prepsf['flxrad'][sel],
		                                colname[3] : prepsf['ell'][sel],
		                                colname[4] : data_psf['fwhm'][sel],
		                                colname[5] : data_psf['ell'][sel]})
		                                # Axis ratio b/a : 1.0/colname[3] vs 1.0-colname[5]

		exec("df_name = 'df_psf_"+flt+"{0:d}'".format(i))
		d_prepsf.to_pickle(dir_psf+df_name+'.pkl')


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
