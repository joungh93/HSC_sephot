#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 4 09:57:04 2021

@author: jlee
"""


import time
start_time = time.time()

import numpy as np
import glob, os
import pandas as pd

import init_cfg as ic


# ----- Reading column information ----- #
f = open("output.param", "r")
ll = f.readlines()
f.close()

sep_cols = [w.split(" ")[0] for w in ll if not w[0] == "#"]
if ic.APHOT:
    n_apers = len(ic.APERs.split(","))
    idx_apers = sep_cols.index(f"MAG_APER({n_apers:d})")
    for i in np.arange(n_apers):
        sep_cols.insert(idx_apers+i, f"MAG_APER{i+1:d}")
    for i in np.arange(n_apers):
        sep_cols.insert(idx_apers+n_apers+i, f"MAGERR_APER{i+1:d}")
    sep_cols.remove(f"MAG_APER({n_apers:d})")
    sep_cols.remove(f"MAGERR_APER({n_apers:d})")


# ----- Reading catalogs & Making DataFrame ----- #
if glob.glob("Catalogs/"):
    os.system("rm -rfv Catalogs/")
else:
    os.system("mkdir Catalogs")

if ic.use_backsub:
    prefix = 'b'
else:
    prefix = ''

for i in np.arange(len(ic.fields)):
    for j in np.arange(len(ic.filters)):
        flt = ic.filters[j].split('-')[1]
        filename = prefix+ic.fields[i]+"-"+flt+".cat"
        sep = np.genfromtxt(prefix+ic.fields[i]+"-"+flt+".cat",
                            dtype=None, encoding="ascii",
                            names=tuple(sep_cols))
        d_sep = pd.DataFrame(sep)
        df_name = "df_sep_"+flt+f"{i:d}"
        d_sep.to_pickle("Catalogs/"+df_name+".pkl")
        

# Printing the running time
print("--- %s seconds ---" % (time.time() - start_time))

