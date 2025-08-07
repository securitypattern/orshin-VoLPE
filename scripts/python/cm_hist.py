#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import pandas as pd

import config.config_scripts.global_vars as gv

from scripts.python.correlations import correlations
from scripts.python.consume_models import consume_model_in, consume_model_pre_post, consume_model_out
from scripts.python.selection_functions import selection_function_in, selection_function_out, selection_function_pre_post
from scripts.python.output_sim import sim_circuit

# Ausiliary functions
def hamming_distance(pre, post):
    hd = 0
    for i in range(len(pre)):
        if(pre[i] != post[i]):
            hd += 1
    return hd

# generates the toggle list for the log passed as argument
#   the toggle list contains in each entry the number of toggles that occur
#   from passing from an old input combination (pre) to a new one (post)
def create_toggle_list(log):
    tl = list()

    with open(log) as lg:
        old_state = ''
        new_state = ''
        toggles = 0
        sim = 0
        for line in lg:
            if line.startswith("BEGIN"):
                toggles = 0
                sim = sim + 1
                new_state = ''
            elif line.startswith("END"):
                tl.append(toggles)
            elif line.startswith("state"):
                new_state = line.split()[1]
            elif line.startswith("out"):
                old_state = new_state
                new_state = line.split()[1]
                toggles = toggles + hamming_distance(old_state, new_state)

    return tl

# calls the create_toggle_list function for the three log files
# generated during the simulation step
def create_toggle_lists(logs):
    toggle_lists = list()

    for log in logs:
        tl = create_toggle_list(log)
        toggle_lists.append(tl)

    return toggle_lists

# takes as input three toggle lists and generates a histogram for each of them
# containg all the different toggle numbers and their occurance
def create_toggles_hist(toggles):
    data = {}
    data_del = {}
    data_in_del = {}

    for e in toggles[0]:
        if e in data:
            val = data.get(e)
            data.update({e: val+1})
        else:
            data.update({e: 1})
    
    for e in toggles[1]:
        if e in data_del:
            val = data_del.get(e)
            data_del.update({e: val+1})
        else:
            data_del.update({e: 1})
    
    for e in toggles[2]:
        if e in data_in_del:
            val = data_in_del.get(e)
            data_in_del.update({e: val+1})
        else:
            data_in_del.update({e: 1})


    p = pd.DataFrame(data.values(), columns=["Toggles"])

    p_del = pd.DataFrame(data_del.values(), columns=["Toggles"])

    p_in_del = pd.DataFrame(data_in_del.values(), columns=["Toggles"])

    return p, p_del, p_in_del

# create_il create a list containing the inputs used for the simulation
# which are read from the input.dat file generated in previous steps
def create_il(in_len):
    il = list()
    f = '0' + str(2*in_len) + 'b'
    
    with open("./tmp/config/inputs.dat", "r") as inputs:
        pre = inputs.readline()
        post = inputs.readline()
        while (pre) and (post):
            num = int(pre)*pow(2, in_len)+int(post)
            s = format(num, f)
            il.append(s)
            pre = inputs.readline()
            post = inputs.readline()

    return il

# create_ol simulates the ideal circuit with the sim_circuit function 
# (defined by the used) and saves the outputs in ol
def create_ol(out_len):
    ol = list()
    f = '0' + str(out_len) + 'b'
    file_len = gv.simulations

    fn_in = "./tmp/config/inputs.dat"
    with open(fn_in, "r") as inputs:
        for l in range(file_len):
            next(inputs)
            post = inputs.readline()
            num = sim_circuit(int(post))
            s = format(num, f)
            ol.append(s)

    return ol

# two lists are used to calculate the correlations with the number of toggles of each simulation
#   - post:     the consume model uses only the post values of the simulation
#   - pre_post: the consume model uses the pre and post values of the simulation
# sel_func and consume_model can be changed by the user

# (i.e. the sel_func takes every single input and the consume model calculates its hamming weight)
def create_post(il):
    post = selection_function_in(il)
    result = consume_model_in(post)

    return result

def create_post_out(ol):
    post = selection_function_out(ol)
    result = consume_model_out(post)
    return result

# (i.e. the sel_func takes the pre and post value of every single input
# and the consume model combines them and calculates their hamming distance)
def create_pre_post(il):
    pre, post = selection_function_pre_post(il)
    result = consume_model_pre_post(pre, post)

    return result

def create_cm_hist(logs, out_corr):

    # the list containing the number of toggles for each simulation is created
    toggles = create_toggle_lists(logs)

    # the histograms for the toggle lists generated above are created
    t_df = create_toggles_hist(toggles)

    t_len = gv.in_size

    il = create_il(int(t_len))

    HW_inputs = create_post(il)
    HD_inputs = create_pre_post(il)
    
    # the correlations are calculated using the pearsons correlation
    corr_HW = correlations(toggles, HW_inputs)
    corr_HD = correlations(toggles, HD_inputs)

    index = ["no delays", "gate delays", "gate+inputs delay"]
    data = dict()
    for i in range(len(corr_HW)):
        key = "HW input" + str(i)
        data[key] = corr_HW[i]
        
    for i in range(len(corr_HD)):      
        key = "HD input" + str(i)
        data[key] = corr_HD[i]

    if out_corr:
        ol = create_ol(int(gv.out_size))
        HW_outputs = create_post_out(ol)
        corr_HW_out = correlations(toggles, HW_outputs)

        for i in range(len(corr_HW_out)):
            key = "HW output" + str(i)
            data[key] = corr_HW_out[i]

    df = pd.DataFrame(data=data, index=index)

    return df, t_df[0], t_df[1], t_df[2]
