#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

class RelapRePattern:
    """
    Regex patterns for relap cards.
    """
    card = re.compile(r"^(\d+).*")                              # any relap5 card (except title card)
                                                                # group1: card number
    hyd_comp = re.compile(r"^(\d{3})(\d{4} .*)")                # hydraulic component cards
                                                                # group1: comp, group2: else
    hyd_comp_type = re.compile(r"^(\d{3})0{4} +\w+ +(\w+)")     # hydraulic component type cards(CCC0000)
                                                                # group1: comp, group2: type
    junc_geo = re.compile(r"^(\d{3})\d{4} +(\d{3})\d{6} +(\d{3})\d{6}.*")
                                                                # junction geometry cards
                                                                # group1: comp, group2: from, group3: to

def generate_loop2_codes():
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
    output_lines = []
    line_couter = 0
    processed_counter = 0
    with open(loop1_filepath, 'r', encoding="utf-8",) as f:
        # process each line
        for line in f:
            line_couter += 1
            line = line.strip()
            matched = re.match(RelapRePattern.hyd_comp, line)
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
                junc_matched = re.match(RelapRePattern.junc_geo, processed_line)
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


def check_input_errors(filename : str):
    """
    Help relap input cards writers to find input errors which cannot be detected by the relap program.
    This function will warn users if
    1. any reduplicated card number exist;
    2. tow junctions have the same 'from' and 'to' parameters;
    (Pending)3. tow defferent component numbers appear in adjacent lines;
    """
    exist_cards = set()
    exist_hyd_comp = set()
    # A dict to store connections relationship of junctions.
    # The smaller one of the numbers('from' & 'to') of Volumes connected by the junctions is the key.
    # Its corresponding value is a set, and the bigger number is one element of the set.
    junc_relation = {}
    n_junctions = 0

    n_warnings = 0
    with open(filename, 'r', encoding='utf-8') as f:
        print("-------------------- start checking ----------------------")
        i_cline = 0     # index for the current line
        for line in f:
            i_cline += 1
            line = line.strip()

            if line == "": continue     # blank line
            if line[0] =="*": continue  # comment line
            if line[0] =="=": continue  # title line
            if line[0] ==".": continue  # terminator line

            card = re.match(RelapRePattern.card, line)
            if not card:                # not a valid card
                n_warnings += 1
                print("{n} - Line {i}: invalid card.".format(n=n_warnings, i=i_cline))
                continue
            card_num = card.group(1)

            # check whether the card is reduplicated
            if card_num in exist_cards:
                n_warnings += 1
                print("{n} - Line {i}: card {c} is reduplicated.".format(
                    n=n_warnings, i=i_cline, c=card_num))
                continue
            exist_cards.add(card_num)

            hyd_comp_type_card = re.match(RelapRePattern.hyd_comp_type, line)
            if hyd_comp_type_card:
                # a hydraulic component name&type card
                exist_hyd_comp.add(hyd_comp_type_card.group(1))

            hyd_geo_card = re.match(RelapRePattern.junc_geo, line)
            if hyd_geo_card:
                # a junction geometry card
                # store connection relationship
                (_, from_num, to_num) = hyd_geo_card.groups()
                from_num = int(from_num)
                to_num = int(to_num)
                if from_num == to_num:
                    n_warnings += 1
                    print("{n} - Line {i}: 'from'&'to' are identical.".format(
                        n=n_warnings, i=i_cline, c=card_num))
                    continue
                elif from_num < to_num:
                    key, val = from_num, to_num
                else:
                    key, val = to_num, from_num

                val_set = junc_relation.setdefault(key, set())
                if val in val_set:
                    n_warnings += 1
                    print("{n} - Line {i}: reduplicated connection relationship between {f} and {t}".format(
                        n=n_warnings, i=i_cline, f=from_num, t=to_num))
                    continue
                else:
                    n_junctions += 1
    
    # print out check results
    print("------------------ checking completed --------------------")
    print("Lines checked:\t{}".format(i_cline))
    print("Lines of cards:\t{}".format(len(exist_cards)))
    print("Number of hydraulic components:\t{}".format(len(exist_hyd_comp)))
    print("Number of explicitly defined junctions:\t{}".format(n_junctions))
    if n_warnings>0:
        print("{} promblems found. They have been printed above.".format(n_warnings))
    else:
        print("No problem found.")
    print("----------------------------------------------------------")
