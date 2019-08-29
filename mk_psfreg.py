#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:48:22 2019

@author: jlee
"""


import numpy as np
import init_patch as ip


band = ['G', 'R', 'I']

for i in np.arange(len(ip.patchstr_dir)):
	for j in band:
		data_psf = np.genfromtxt('psf_'+j+ip.patchstr_sex[i]+'.cat', dtype=None,
			                     encoding='ascii', usecols=(5,6), names=('x','y'))
		if (data_psf.size > 10):
			f = open('psf_'+j+ip.patchstr_sex[i]+'.reg','w')
			for k in np.arange(len(data_psf)):
				f.write('{0:.3f}  {1:.3f}'.format(data_psf['x'][k], data_psf['y'][k])+'\n')
			f.close()

