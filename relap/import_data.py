#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pathlib import Path
import os

import numpy as np
import pandas as pd


def stripf_preprocess(filename=r'..\model\stripf'):
    '''
    Reform stripf file. Remove linefeeds for a data row. 
    '''
    filepath = Path(os.path.abspath(filename))
    if not filepath.exists():
        raise Exception("{0} doesn't exist".format(filepath))
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


def read_processed(filename=r'..\model\stripf_tr.txt'):
    """
    From processed stripf file (by stripf_preprocess()) import data into pandas.Dataframe object.
    """
    filename = Path(os.path.abspath(filename))
    if not Path(filename).exists():
        raise Exception("{0} doesn't exist".format(Path(filename)))
    strip_file = Path(filename).with_name('strip')

    col_names = [0]
    with open(strip_file, 'r') as f:
        # from strip read each variables' codes (1xxx).
        for line in f:
            code = re.match(r'^1\d{3}', line.strip())
            if code:
                col_names.append(int(code.group()))
    col_names.sort()

    with open(filename, 'r') as f:
        # read the number of lines
        plotinf_line = re.match(r"^  plotinf\s+([0-9]+).+", f.readlines()[2])
        if plotinf_line:
            n_col = int(plotinf_line.group(1))
        else:
            raise Exception("Can't read the plotinf line. Make sure the stripf file is corrective.")
        f.seek(0)
        converters_dict = dict(zip(range(n_col), [data_converter]*n_col))
        df = pd.read_table(f, sep=r'\s+', 
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


def read_stripf(filename=r'..\model\stripf'):
    """
    From raw stripf file import data into pandas.Dataframe object.
    """
    filename = Path(os.path.abspath(filename))
    prf = stripf_preprocess(filename)
    df = read_processed(prf)
    return df
