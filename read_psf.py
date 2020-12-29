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

colname = ['fwhm', 'flxrad', 'ell']

for i in np.arange(len(ic.fields)):
	for j in np.arange(len(ic.filters)):
		flt = ic.filters[j].split('-')[1]
		data_psf = np.genfromtxt('psf_'+ic.fields[i]+'-'+flt+'.cat', dtype=None,
                                 encoding='ascii', usecols=(0,5,6), names=('num','x','y'))
		idx = data_psf['num']-1

		if (data_psf.size > 10):

			# Writing a region file
			f = open('psf_'+ic.fields[i]+'-'+flt+'.reg','w')
			for k in np.arange(len(data_psf)):
				f.write(f"{data_psf['x'][k]:.3f}  {data_psf['y'][k]:.3f}"+'\n')
			f.close()

			# Reading a SExtractor catalog
			prepsf = np.genfromtxt('prepsfex_'+ic.fields[i]+'-'+flt+'.cat', dtype=None,
			                       encoding='ascii', usecols=(1600,1601,1604,1605,1606),
			                       names=('x','y','flxrad','fwhm','ell'))

			d_prepsf = pd.DataFrame(data = {colname[0] : prepsf['fwhm'][idx],
			                                colname[1] : prepsf['flxrad'][idx],
			                                colname[2] : prepsf['ell'][idx]})
			exec("df_name = 'df_psf_"+flt+"{0:d}'".format(i))
			d_prepsf.to_pickle(df_name+'.pkl')


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
