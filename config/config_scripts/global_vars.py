#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

simulations = 0
in_size = 0
rand_size = 0
out_size = 0
full = 'y'

def new_in_size(new_val):
    global in_size 
    in_size = new_val

def new_rand_size(new_val):
    global rand_size
    rand_size = new_val

def new_simulations(new_val):
    global simulations
    simulations = new_val

def new_out_size(new_val):
    global out_size
    out_size = new_val

def new_full(new_val):
    global full
    full = new_val