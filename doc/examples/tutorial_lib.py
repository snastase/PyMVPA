#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import os
import numpy as N

# later replace with
from mvpa.suite import *


def get_haxby2001_data(path='pymvpa-exampledata'):
    attr = SampleAttributes(os.path.join(path, 'attributes_literal.txt'))
    ds = fmri_dataset(samples=os.path.join(path, 'bold.nii.gz'),
                      labels=attr.labels, chunks=attr.chunks,
                      mask=os.path.join(path, 'mask_vt.nii.gz'))

    # do chunkswise linear detrending on dataset
    ds = ds.get_mapped(PolyDetrendMapper(polyord=1, chunks='chunks',
                                    inspace='time_coords'))

    # mark the odd and even runs
    rnames = {0: 'even', 1: 'odd'}
    ds.sa['runtype'] = [rnames[c % 2] for c in ds.sa.chunks]

    # compute the mean sample per condition and odd vs. even runs
    # aka "constructive interference"
    ds = ds.get_mapped(mean_group_sample(['labels', 'runtype']))

    # zscore dataset relative to baseline ('rest') mean
    # XXX needs fixing: perchunk -> chunks, + attr for labels
    zscore(ds, perchunk=True, baselinelabels=['rest'])

    # exclude the rest condition from the dataset
    ds = ds[ds.sa.labels != 'rest']

    return ds


def get_haxby2001_clf():
    clf = kNN(k=1, dfx=oneMinusCorrelation, voting='majority')
    return clf

