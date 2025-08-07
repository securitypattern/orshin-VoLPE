#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import os
import config.config_scripts.global_vars as gv

def gen_in():
    with open("./tmp/config/inputs.dat", "a") as inputs:
        # potential old inputs are truncated
        inputs.truncate(0)

        # the full parameter has two possible values
        #   - y: all the possible input combinations have to be simulated
        #   - n: a subset of all simulations is simulated -> the inputs are generated randomically
        if(gv.full == 'y'):
            sim = 2**(gv.in_size)
            for i in range(0, sim):
                for j in range(0, sim):
                    inputs.write(str(i) + "\n" + str(j) + '\n')
                    
        else:
            bytes_to_gen = int((gv.in_size)/8)
            r = int((gv.in_size)%8)
            if r != 0:
                bytes_to_gen = bytes_to_gen + 1

            for i in range(0, 2*(gv.simulations)):
                rand = int.from_bytes(os.urandom(bytes_to_gen), "big") % (2**(gv.in_size))
                inputs.write(str(rand) + "\n")