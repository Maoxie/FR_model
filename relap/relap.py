#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path


# file path
root_path = os.path.dirname(os.path.dirname(__file__))    # project root path
# put model input cards in the "./model" folder
# os.chdir(os.path.join(__file__))
in_out_dir = os.path.join(root_path,'model')
relap_bin_exe = os.path.join(root_path,'relap_bin','relap5.exe')     # main relap5 executatble file

def run_model(opt:str):
    # delete outdta for a "new" question before running
    if opt.lower()=='new':
        tmp = Path(in_out_dir) / 'outdta'
        if os.path.isfile(tmp):
            os.remove(tmp)
            print("Outdta has been removed.")

    run_options = {
        'i': "'{}'".format(os.path.join(in_out_dir, 'indta')),
        'o': "'{}'".format(os.path.join(in_out_dir, 'outdta')),
        'r': "'{}'".format(os.path.join(in_out_dir, 'rstplt')),
        's': "'{}'".format(os.path.join(in_out_dir, 'stripf'))
    }

    options_str = '-i {i} -o {o} -r {r} -s {s}'.format(
        i=run_options['i'], 
        o=run_options['o'], 
        r=run_options['r'],
        s=run_options['s'],
    )
    print("----start run model----")
    subprocess.call('{relap} {option}'.format(relap=relap_bin_exe, option=options_str))
    print("----complete model----")

def run_strip():
    run_options = {
        'i': "'{}'".format(os.path.join(in_out_dir, 'strip')),
        'o': "'{}'".format(os.path.join(in_out_dir, 'outdta')),
        'r': "'{}'".format(os.path.join(in_out_dir, 'rstplt')),
        's': "'{}'".format(os.path.join(in_out_dir, 'stripf'))
    }
    options_str = '-i {i} -o {o} -r {r} -s {s}'.format(
        i=run_options['i'], 
        o=run_options['o'], 
        r=run_options['r'],
        s=run_options['s'],
    )
    subprocess.call('{relap} {option}'.format(relap=relap_bin_exe, option=options_str))
    print("----complete strip----")
