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
from xml.etree.ElementTree import parse
import init_cfg as ic

colname = ['ID', 'fwhm_sep', 'flxrad_sep', 'ba_sep', 'fwhm_psf', 'ba_psf']
dir_psf = "PSFEx/"

for i in np.arange(len(ic.fields)):
	for j in np.arange(len(ic.filters)):
		
		print("Reading PSFEx data of "+ic.fields[i]+" ("+ic.filters[j]+") ...")

		# ----- For PSF-selected sources ----- #
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

		# Writing pickle files of PSF-selected sources
		d_prepsf = pd.DataFrame(data = {colname[0] : data_psf['num'][sel],
			                            colname[1] : prepsf['fwhm'][sel],
		                                colname[2] : prepsf['flxrad'][sel],
		                                colname[3] : 1./prepsf['ell'][sel],
		                                colname[4] : data_psf['fwhm'][sel],
		                                colname[5] : 1.-data_psf['ell'][sel]})
		                                # Axis ratio b/a : 1.0/colname[3] vs 1.0-colname[5]

		exec("df_name = 'df_psf_"+flt+"{0:d}'".format(i))
		d_prepsf.to_pickle(dir_psf+df_name+'.pkl')


		# ----- For PSFEx results ----- # 

		# Reading XML files (single field)
		tree = parse(dir_psf+"psf_"+ic.fields[i]+"-"+flt+".xml")
		root = tree.getroot()
		# Please check the tree view of the XML file in advance.
		# (https://www.xmlviewer.org/)
		tb1 = root.findall("RESOURCE")[0].findall("RESOURCE")[0].findall("TABLE")[0]
		tb1_field = tb1.findall("FIELD")
		tb1_data = tb1.findall("DATA")[0].findall("TABLEDATA")[0].findall("TR")[0].findall("TD")
		n_field = len(tb1_field)
		fld_name, fld_dtype, fld_data = [], [], []
		for ff in np.arange(n_field):
			fld_name.append(tb1_field[ff].attrib['name'])
			fld_dtype.append(tb1_field[ff].attrib['datatype'])
		for ff in np.arange(n_field):
			if (fld_dtype[ff] == 'char'):
				key_data = tb1_data[ff].text
			elif (fld_dtype[ff] == 'int'):
				key_data = np.int(tb1_data[ff].text)
			elif (fld_dtype[ff] == 'float'):
				key_data = np.float(tb1_data[ff].text)
			fld_data.append(key_data)

		d_psf = pd.DataFrame(data=[fld_data], columns=fld_name)
		exec("df_name = 'xml_psf_"+flt+"{0:d}'".format(i))
		d_psf.to_csv(dir_psf+df_name+'.csv')


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))



# tree = parse("PSFEx/psf_M81_2-R.xml")
# root = tree.getroot()

# tb1 = root.findall("RESOURCE")[0].findall("RESOURCE")[0].findall("TABLE")[0]

# tb1_field = tb1.findall("FIELD") 
# for ff in tb1_field: 
#     print(ff.attrib) 

# tb1_data = tb1.findall("DATA")[0].findall("TABLEDATA")[0].findall("TR")[0].findall("TD")
# for gg in tb1_data: 
#     print(gg.text) 
