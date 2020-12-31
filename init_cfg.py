#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:35:13 2020

@author: jlee
"""


import glob


# ----- For coadding HSC processed images ----- #
dir_coadd = "/data/jlee/HSCv6/M81/Bell/Red/rerun/object/deepCoadd-results/"    # Path for 'deepCoadd-results'
filters = [f.split("/")[-1] for f in sorted(glob.glob(dir_coadd+"HSC-*"))]
tracts = list(set([f.split("/")[-1] for f in sorted(glob.glob(dir_coadd+"HSC-*/*"))]))
fields = ["M81_1", "M81_2"]    # HSC field names
# Check the center coordinates by displaying images with DS9
ra0 = ["09:58:27.33", "10:03:04.23"]
dec0 = ["+69:44:49.5", "+68:46:21.6"]
# Command: ds9 -mosaic wcs [dir_coadd]/HSC-[filter]/[tract]/*,*/calexp*.fits &
pixscale = 0.168   # arcsec/pix
isize = 1.6*3600.0 / pixscale    # Image size (total: 1.6 arcdeg)
upper_limit = 10.0    # upper limit of pixel values
BACKS_swp = 64    # BACK_SIZE for SWarp configuration


# ----- Photometric parameters ----- #

## General
use_backsub = True  # if True, SExtractor photometry will be applied to background-subtracted images
MAG0 = 27.0  # MAG_ZEROPOINT
SEEING0 = 0.7  # SEEING_FWHM
GAIN0 = [[12600, 9900, 9900],
         [12600, 9900, 9900]]  # effective gain (n_fields x n_filters)

## PSFEx
THRES_psf = 10.0  # DETECT_THRESH
FWHMR_psf = [3.0, 5.0]  # SAMPLE_FWHMRANGE
MINSN_psf = 10.0  # SAMPLE_MINSN
MAXEL_psf = 0.18  # SAMPLE_MAXELLIP

## SExtractor
MINAR_sep = 5  # DETECT_MINAREA
THRES_sep = 2.0  # DETECT_THRESH
FILTR_sep = '/usr/share/sextractor/tophat_5.0_5x5.conv'
DEBLN_sep = 32  # DEBLEND_NTHRESHOLD
DEBLM_sep = 0.005  # DEBLEND_MINCONT
APHOT = False  # if True, you will do aperture photometry (please revise output.param)
APERs = "4.0,6.0,8.0,10.0,12.0,18.0,24.0,33.3"  # apertures for MAG_APER (string)
BACKS_sep = 32  # BACK_SIZE
