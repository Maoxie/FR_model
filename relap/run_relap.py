#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from pathlib import Path


# file path
root_path = Path(os.path.dirname(os.path.dirname(__file__)))    # project root path
# put model input cards in the "./model" folder
in_out_dir = root_path / 'model'
relap_bin_exe = root_path / 'relap_bin' / 'relap5.exe'      # main relap5 executatble file

def run_new_model():
    # delete outdta for a "new" question before running
    i_file = in_out_dir / 'indta'
    o_file = in_out_dir / 'outdta'
    r_file = in_out_dir / 'rstplt'
    for filepath in [o_file, r_file]:
        try:
            filepath.replace(o_file.with_name('{}.old'.format(filepath.name)))
            print("{0} has been renamed as {0}.old.".format(filepath.name))
        except:
            pass

    run_options = {
        '-i': '"{}"'.format(i_file),
        '-o': '"{}"'.format(o_file),
        '-r': '"{}"'.format(r_file),
    }
    options_str = ' '.join([ key +' '+ value for key,value in run_options.items()])
    call_str = '{relap} {option}'.format(relap=relap_bin_exe, option=options_str)
    print("----start run new model----")
    print("-->> {}".format(call_str))
    subprocess.call(call_str)
    print("----complete model----")

def run_strip():
    i_file = in_out_dir / 'strip'
    o_file = in_out_dir / 'outdta'
    r_file = in_out_dir / 'rstplt'
    run_options = {
        'i': "'{}'".format(i_file),
        'o': "'{}'".format(o_file),
        'r': "'{}'".format(r_file),
    }
    options_str = '-i {i} -o {o} -r {r}'.format(
        i=run_options['i'], 
        o=run_options['o'], 
        r=run_options['r'],
    )

    print("----start strip----")
    subprocess.call('{relap} {option}'.format(relap=relap_bin_exe, option=options_str))
    print("----complete strip----")
