#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path
import os

import numpy as np
import pandas as pd


def stripf_preprocess(filename):
    '''
    Reform stripf file. Remove linefeeds for a data row. 
    '''
    filepath = Path(filename)
    with open(filename, 'r') as f:
        lines = f.readlines()
        new_row_pattern = re.compile(r'^  plot[a-z]{3}')    # pattern for the begin of a new row of record

        # initialization
        processed_lines = lines[:3]

        new_row = []
        for line in lines[3:]:
            if re.match(new_row_pattern, line):
                # start of a new row of record
                if new_row:
                    processed_lines.append(''.join(new_row))    # save a fully completed row
                new_row = line                      # start a new row
            else:
                # following lines of a row of record
                new_row = new_row.strip('\n')+line              # append following lines
        if new_row:
            processed_lines.append(''.join(new_row))    # save the last row

    # save file
    savepath = filepath.with_name('stripf_tr.txt')
    with open(savepath, 'w') as wf:
        wf.writelines(processed_lines)
    return savepath


def read_processed(filename):
    """
    From processed stripf file (using stripf_preprocess()) import data into pandas.Dataframe object.
    """
    n_col = 31
    col_names = range(n_col)
    converters_dict = dict(zip(range(n_col), [data_converter]*n_col))
    df = pd.read_table(filename, sep=r'\s+', 
                        skiprows=3,
                        header=None,
                        names=col_names,
                        converters=converters_dict)
    return df
    

def data_converter(rec : str):
    """
    Convert number string into float.
    """
    rec = rec.strip()
    if re.match(r'[0-9.Ee]+', rec):
        return float(rec)
    else:
        return rec


def read_stripf(filename):
    """
    From raw stripf file import data into pandas.Dataframe object.
    """
    tmp = stripf_preprocess(filename)
    df = read_processed(tmp)
    os.remove(tmp)
    return df
