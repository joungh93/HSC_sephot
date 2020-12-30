# HSC_sephot
(updated on 2020. 12. 30.)


## Description
[PSFEx](https://www.astromatic.net/software/psfex) + [SExtractor](https://www.astromatic.net/software/sextractor) photometry of the images obtained with [Subaru/Hyper Suprime-Cam (HSC)](https://www.subarutelescope.org/Observing/Instruments/HSC/index.html)


## Example data sets
* Field name: 'M81_1', 'M81_2'
* Observer: Eric Bell
* Retrieved from [SMOKA](https://smoka.nao.ac.jp/)
* Reduction pipeline: [hscPipe6](https://hsc.mtk.nao.ac.jp/pipedoc/pipedoc_6_e/index.html)


## Prerequisites
* [PSFEx (ver 3.22.1)](https://psfex.readthedocs.io/en/latest/)
* [SExtractor (ver 2.19.5)](https://www.astromatic.net/pubsvn/software/sextractor/trunk/doc/sextractor.pdf) and its configuration files: [prepsfex.param](https://github.com/joungh93/HSC_sephot/blob/master/prepsfex.param), [output.param](https://github.com/joungh93/HSC_sephot/blob/master/output.param), [prepsfex.sex](https://github.com/joungh93/HSC_sephot/blob/master/prepsfex.sex), [config.sex](https://github.com/joungh93/HSC_sephot/blob/master/config.sex)
* [SWarp (ver 2.38.0)](https://www.astromatic.net/pubsvn/software/swarp/trunk/doc/swarp.pdf)
* [The ElementTree XML](https://docs.python.org/3/library/xml.etree.elementtree.html)


## Workflows
```
cd /your_working_directory/
git clone https://github.com/joungh93/HSC_sephot.git
```

After revising ``init_cfg.py``, the following sequence of commands will work well.

```
$ tmux
$ ipython
> run mk_coadd.py
> run mkscr_psfex.py
> run read_psf.py
> run plt_psf.py
> run mk_mchcomb.py
> run mkscr_sephot.py
(Ctrl + b + d)
```


## Future works
* 
