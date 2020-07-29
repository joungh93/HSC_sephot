# HSC_sephot
(updated on 2020. 07. 29.)


## Description
[PSFEx](https://www.astromatic.net/software/psfex) + [SExtractor](https://www.astromatic.net/software/sextractor) photometry of the images obtained with [Subaru/Hyper Suprime-Cam (HSC)](https://www.subarutelescope.org/Observing/Instruments/HSC/index.html)


## Example data sets
* Field name: 'M81_1', 'M81_2'
* Observer: Eric Bell
* Retrieved from [SMOKA](https://smoka.nao.ac.jp/)
* Reduction pipeline: [hscPipe6](https://hsc.mtk.nao.ac.jp/pipedoc/pipedoc_6_e/index.html)


Prerequisite
-----
* For PSFEx : prepsfex.param, prepsfex.sex, config.psfex
* For SExtractor : output.param, config.sex
* For IRAF/PyRAF tasks : pyraf (in Anaconda 3)


Running sequence
-----
init_patch.py    # Initial declaration of patches

mk_single.py    # HSC multiple extension images -> single extension images

mkscr_psfex.py    # Running PSFEx w/ psfex_all.sh

mk_psfreg.py    # Writing region files of PSF stars from PSFEx

mk_mchcomb.py    # Making PSF-matched images and combining them

mkscr_sephot.py    # Running SExtractor DUAL mode photometry

