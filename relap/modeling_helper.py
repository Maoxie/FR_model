#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path


def generate_loop2_codes() -> str:
    """
    Generate codes for loop#2, from a given loop#1 codes file(loop1codes.txt).
    This function is going to change components' number in loop#1 to 
    components' number in loop #2 according to a reference table(二回路组件编号对照表.csv).
    """
    loop1_filename = 'loop1codes.txt'
    ref_table_filename = u'二回路组件编号对照表.csv'
    output_filename = 'loop2codes_generated.txt'

    in_out_path = Path(__file__).parents[1] / 'model'

    loop1_filepath = in_out_path / loop1_filename
    ref_table_filepath = in_out_path / ref_table_filename 
    if not ( loop1_filepath.exists() and ref_table_filepath.exists() ):
        raise Exception("{0} or {1} doesn't exist.".format(loop1_filename, ref_table_filename))
    output_filepath = in_out_path / output_filename
    
    # read reference table
    ref_table = {}
    import csv
    with open(ref_table_filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        _head_row = next(reader)
        for row in reader:
            if row[0] not in ref_table:     # in python3, has_key() has been deleted.
                ref_table[row[0]] = row[1]
            else:
                raise Exception('Duplicated key: {0} already exist.'.format(row[0]))
    
    # process loop1codes.txt
    import re
    output_lines = []
    line_couter = 0
    processed_counter = 0
    with open(loop1_filepath, 'r', encoding="utf-8",) as f:
        # patterns
        hyd_cards_pattern = re.compile(r"^(\d{3})(\d{4} .*)")     # pattern for hydraulic component card
        # type_pattern = re.compile(r"^(\d{3})0{4} +\w+ +(\w+)")    # pattern for CCC0000 card(component name & type)
        junc_pattern = re.compile(r"^(\d{3})010[1-9] +(\d{3})\d{6} +(\d{3})\d{6}.*")    # group1: comp, group2: from, group3: to
        # process each line
        for line in f:
            line_couter += 1
            line = line.strip()
            matched = re.match(hyd_cards_pattern, line)
            if matched:
                # Hydraulic component card
                comp_num = matched.group(1)
                try:
                    rep_comp_num = ref_table[comp_num]
                except KeyError:
                    raise Exception("Component {} does not in reference table.".format(comp_num))
                # replace component number
                processed_line = rep_comp_num + matched.group(2)
                # replace 'from' and 'to' parameters for junction components
                junc_matched = re.match(junc_pattern, processed_line)
                if junc_matched:
                    (_, from_num, to_num) = junc_matched.groups()
                    rep_from_num = ref_table[from_num]
                    rep_to_num = ref_table[to_num]
                    (from_i, _) = junc_matched.span(2)
                    (to_i, _) = junc_matched.span(3)
                    processed_line = \
                        processed_line[:from_i] + rep_from_num + \
                        processed_line[from_i+3:to_i] + rep_to_num + \
                        processed_line[to_i+3:]
                # append to result list
                output_lines.append(processed_line)
                processed_counter += 1
                # TODO:
            else:
                output_lines.append(line)
        print("-- Total lines: {0}\n-- {1} line(s) processed, {2} line(s) not changed.".format(
            line_couter, processed_counter, line_couter-processed_counter))
    
    # results output
    with open(output_filepath, 'w', encoding='utf-8') as outf:
        outf.writelines('\n'.join(output_lines))

    # with open(filepath, 'r') as f_loop1:



