#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

from tkinter import N
import config.config_scripts.global_vars as gv

n = 1

# consume model functions called from the main programm.
# do not change the signature of this functions!!
def selection_function_in(il):
    # number of bits grouped together
    n_in  = n
    return sel_func_n(il, n_in)

def selection_function_out(ol):
    # number of bits grouped together
    n_out  = n
    return sel_func_out_n(ol, n_out)

def selection_function_pre_post(il):
    # number of bits grouped together
    n_in  = n
    return sel_func_pre_post_n(il, n_in)
#---------------------------------------------------------------

# selection function that can be changed by the user:
# takes as input the input list read from input.dat
# returns a list of the selected post values
def sel_func_n(il, n_in):
    result = list()

    if((gv.in_size % n_in) != 0):
        print("Uneven number of inputs. Choose another selection function.")
        exit(1)

    size = int(gv.in_size / n_in)

    for i in range(size):
        l = list()
        result.append(l)

    post = ''
    for i in range(len(il)):
        for input in range(size):
            for c in range(n_in):
                post += il[i][(gv.in_size) + input*n_in+c]
            result[input].append(post)
            post=''
        
    return result

def sel_func_out_n(ol, n_out):
    result = list()

    if((gv.out_size % n_out) != 0):
        print("Uneven number of Outputs. Choose another selection function.")
        exit(1)

    size = int(gv.out_size / n_out)
    
    for i in range(size):
        l = list()
        result.append(l)

    post = ''
    for i in range(len(ol)):
        for output in range(size):
            for c in range(n_out):
                post += ol[i][output*n_out+c]
            result[output].append(post)
            post=''
    
    return result

# selection function that can be changed by the user:
# takes as input the input list read from input.dat
# returns a list of the selected pre and post values
def sel_func_pre_post_n(il, n_in):
    pre = list()
    post = list()

    if((gv.in_size % n_in) != 0):
        print("Uneven number of inputs. Choose another selection function.")
        exit(1)

    size = int(gv.in_size / n_in)

    for i in range(size):
        a = list()
        b = list()
        pre.append(a)
        post.append(b)
    
    pr = ''
    po = ''
    for i in range(len(il)):
        for input in range(size):
            for c in range(n_in):
                pr += il[i][input*n_in+c]
                po += il[i][(gv.in_size) + input*n_in+c]

            pre[input].append(pr)
            post[input].append(po)
            pr = ''
            po = ''
        
    return pre, post