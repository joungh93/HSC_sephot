#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 11:12:10 2020

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import glob, os
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
import pandas as pd
from scipy import stats
import init_cfg as ic


# ----- Reading the PSF pickle files ----- #
dir_psf = "PSFEx/"
psf_pkl = glob.glob(dir_psf+'df_psf*.pkl')
psf_pkl = sorted(psf_pkl)

for i in np.arange(len(psf_pkl)):
    f_name = psf_pkl[i].split('_')[-1].split('.pkl')[0]
    df_psf = pd.read_pickle(psf_pkl[i])
    xml_psf = pd.read_csv(dir_psf+"xml_psf_"+f_name+".csv")

    # ----- Figure : PSF FWHM + PSF FLUX_RADIUS + b/a ----- #
    fs, lw = 17.5, 2.25

    fig = plt.figure(i+1, figsize=(10,9))
    plt.suptitle('PSF-selected sources ('+f_name+', {0:d})'.format(len(df_psf)),
                 x=0.5, y=0.96, ha='center', va='center', fontsize=20.0, fontweight='bold')
    gs = GridSpec(2, 2, left=0.10, bottom=0.09, right=0.97, top=0.93,
                  hspace=0.09, wspace=0.10, height_ratios=[1.,1.], width_ratios=[1.,1.])

    # ----- Axis setting ----- #
    colname = ['fwhm_sep', 'ba_sep',
               'fwhm_psf', 'ba_psf']
    xl = ["FWHM [pix]", r"Axis ratio [$b/a$]"]

    fwhm_tot = np.append(df_psf['fwhm_sep'].values, df_psf['fwhm_psf'].values)
    fmin, fmax = np.percentile(fwhm_tot, [0.01, 99.99])
    fhRange = (fmin, fmax)
    fpRange = (fmin*0.70, fmax/0.95)

    for j in np.arange(len(colname)):
        ax = fig.add_subplot(gs[j//2, j%2])
        plt_Data = df_psf[colname[j]].values
        if (j%2 == 1):
            Nbin, Range = 40, (0.6, 1.0)
        else:
            Nbin, Range = 40, fhRange

        hist = np.histogram(plt_Data, bins=Nbin, range=Range)

        ax.set_ylim([0.0, 1.25*np.max(hist[0])])
        ax.set_yticks([0.0, 0.5*np.max(hist[0]), 1.0*np.max(hist[0])])
        ax.set_yticklabels(['0.0', '0.5', '1.0'], fontsize=fs)

        if (j//2 == 0):
            ax.tick_params(labelbottom=False)
        if (j//2 == 1):
            ax.set_xlabel(xl[j%2], fontsize=fs)
        if (j%2 == 0):
            ax.set_ylabel(r'$N/N_{\rm max}$', fontsize=fs)
            ax.set_xticks(np.arange(10))
            ax.set_xticklabels(np.arange(10), fontsize=fs)
            ax.set_xlim(fpRange)
        if (j%2 == 1):
            ax.set_xticks([0.5,0.6,0.7,0.8,0.9,1.0])
            ax.set_xticklabels([0.5,0.6,0.7,0.8,0.9,1.0], fontsize=fs)
            ax.set_xlim([0.6, 1.0])
            ax.tick_params(labelleft=False)

        ax.tick_params(width=1.5, length=8.0)
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(n=5))
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(n=5))
        ax.tick_params(width=1.5,length=5.0,which='minor')
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(1.5)

        ax.hist(plt_Data, bins=Nbin, range=Range,
                color='dodgerblue', histtype='step', linewidth=lw)

        mod, cnt = stats.mode(plt_Data)
        ax.plot(2*[mod[0]], [0.0, 1.25*np.max(hist[0])], color='red',
                linestyle='--', linewidth=lw-0.25, alpha=0.6)

        # Figure texts
        if (j // 2 == 0):
            ax.text(0.04, 0.95, "SExtractor output", color='k', fontsize=fs, fontweight='bold',
                    ha='left', va='top', transform=ax.transAxes)
        if (j // 2 == 1):
            ax.text(0.04, 0.95, "PSFEx output", color='k', fontsize=fs, fontweight='bold',
                    ha='left', va='top', transform=ax.transAxes)
        if (j == 2):
            ax.text(0.04, 0.50, f"FWHM (2xRh): {xml_psf['FWHM_FromFluxRadius_Mean'].values[0]:.2f} pix",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            # ax.text(0.12, 0.45, f"({xml_psf['FWHM_FromFluxRadius_Min'].values[0]:.2f} - {xml_psf['FWHM_FromFluxRadius_Max'].values[0]:.2f} pix)",
            #         color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.40, f"FWHM (term): {xml_psf['FWHM_Mean'].values[0]:.2f} pix",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            ax.text(0.12, 0.35, f"({xml_psf['FWHM_Min'].values[0]:.2f} - {xml_psf['FWHM_Max'].values[0]:.2f} pix)",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.30, r"Moffat $\beta$: %.2f" %(xml_psf['MoffatBeta_Mean'].values[0]),
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            ax.text(0.12, 0.25, f"({xml_psf['MoffatBeta_Min'].values[0]:.2f} - {xml_psf['MoffatBeta_Max'].values[0]:.2f})",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
        if (j == 3):
            ax.text(0.04, 0.50, f"Axis ratio: {1.0-xml_psf['Ellipticity_Mean'].values[0]:.2f}",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
            ax.text(0.12, 0.45, f"({1.0-xml_psf['Ellipticity_Max'].values[0]:.2f} - {1.0-xml_psf['Ellipticity_Min'].values[0]:.2f})",
                    color='blue', fontsize=fs-7.5, ha='left', va='top', transform=ax.transAxes)
        if (j % 2 == 0):
            ax.text(0.04, 0.85, f"Mode: {mod[0]:.2f} pix", color='red', fontsize=fs-5.0, 
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.18, 0.80, f'({mod[0]*ic.pixscale:.2f}")',color='red', fontsize=fs-5.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.74, f"Median: {np.median(plt_Data):.2f} pix", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.69, f"Mean: {np.mean(plt_Data):.2f} pix", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.64, f"Min: {np.min(plt_Data):.2f} pix", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.59, f"Max: {np.max(plt_Data):.2f} pix", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
        if (j % 2 == 1):
            ax.text(0.04, 0.85, f"Mode: {mod[0]:.2f}", color='red', fontsize=fs-5.0, 
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.79, f"Median: {np.median(plt_Data):.2f}", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.74, f"Mean: {np.mean(plt_Data):.2f}", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.69, f"Min: {np.min(plt_Data):.2f}", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)
            ax.text(0.04, 0.64, f"Max: {np.max(plt_Data):.2f}", color='dimgray', fontsize=fs-6.0,
                    ha='left', va='top', transform=ax.transAxes)

    plt.savefig(dir_psf+'figpsf-'+f_name+'.pdf', dpi=300)
    plt.savefig(dir_psf+'figpsf-'+f_name+'.png', dpi=300)
    plt.close()

    # ax1.plot([np.median(df_psf['fwhm_sep']), np.median(df_psf['fwhm_sep'])], [0.0, 1.15*np.max(hist_fwhm[0])],
 #             '--', color='red', linewidth=lw+0.25, alpha=0.8)
    # ax1.text(0.95, 0.95, '{0:.2f} pix={1:.2f}"'.format(np.median(df_psf['fwhm_sep']), ic.pixscale*np.median(df_psf['fwhm_sep'])),
    #          ha='right', va='top', transform=ax1.transAxes, fontsize=fs, color='r')

    # print('Median seeing FWHM of '+f_name+ \
    #     ' : {0:.2f} pix = {1:.2f} arcsec'.format(np.median(df_psf['fwhm_sep']),
    #                                              ic.pixscale*np.median(df_psf['fwhm_sep'])))


# Printing the running time  
print("--- %s seconds ---" % (time.time() - start_time))
