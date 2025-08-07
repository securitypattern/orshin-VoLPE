#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import config.config_scripts.global_vars as gv

n = 1

# consume model functions called from the main programm.
# do not change the signature of this functions!!
def consume_model_in(post):
    # number of bits grouped together
    n_in  = n
    #return cons_mod(post, gv.in_size, n_in) 
    return cons_mod_sec(post, gv.in_size, n_in) 

def consume_model_out(post):
    # number of bits grouped together
    n_out = n
    #return cons_mod(post, gv.out_size, n_out) 
    return cons_mod_sec(post, gv.out_size, n_out)

def consume_model_pre_post(pre, post):
    # number of bits grouped together
    n_in = n
    #return cons_mod_pre_post(pre, post, n_in)
    return cons_mod_pre_post_sec(pre, post, n_in) 
#---------------------------------------------------------------

# Ausiliary functions
def hamming_weight(post):
    return  post.count("1")

def hamming_distance(pre, post):
    hd = 0
    for i in range(len(pre)):
        if(pre[i] != post[i]):
            hd += 1
    return hd

# hw of the original values (secrets)
def hamming_weight_secret(post):
    return post.count("1")%2

# hd of the original values (secrets)
def hamming_distance_secret(pre, post):
    hd = hamming_distance(pre, post)
    return hd%2

# User defined consume models called from the above fixed functions
# consume model working only on the post values of the simulations
def cons_mod(post, s, n):
    result = list()

    size = int(s / n)

    for i in range(size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(size):
            result[input].append(hamming_weight(post[input][i]))

    return result

# consume model with HW of the secrets
def cons_mod_sec(post, s, n):
    result = list()

    size = int(s / n)

    for i in range(size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(size):
            result[input].append(hamming_weight_secret(post[input][i]))

    return result

# consume model working on the pre and post values of the simulations
def cons_mod_pre_post(pre, post, n):
    result = list()

    size = int(gv.in_size / n)

    for i in range(size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(size):
            result[input].append(hamming_distance(pre[input][i], post[input][i]))

    return result

# MARI: consume model with HD of pre and post of the secrets
def cons_mod_pre_post_sec(pre, post, n):
    result = list()

    size = int(gv.in_size / n)

    for i in range(size):
        l = list()
        result.append(l)

    for i in range(gv.simulations):
        for input in range(size):
            result[input].append(hamming_distance_secret(pre[input][i], post[input][i]))

    return result