
# SExtractor-photometry-HSC-images
-----
PSFEx + Source Extractor photometry of HSC images using two fields of gri images


# Basics
-----
Field name : 'M81_1', 'M81_2'

Observer : Bell

Retrieved from SMOKA

Reduced using hscPipe ver 6.0.7


# Prerequisite
-----
For PSFEx : prepsfex.param, prepsfex.sex, config.psfex

For SExtractor : output.param, config.sex

For IRAF/PyRAF tasks : pyraf (in Anaconda 3)


# Running sequence
-----
init_patch.py    # Initial declaration of patches

mk_single.py    # HSC multiple extension images -> single extension images

mkscr_psfex.py    # Running PSFEx w/ psfex_all.sh

mk_psfreg.py    # Writing region files of PSF stars from PSFEx

mk_mchcomb.py    # Making PSF-matched images and combining them

mkscr_sephot.py    # Running SExtractor DUAL mode photometry

