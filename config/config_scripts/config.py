#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import math
import os
import warnings
from random import random

from scripts.python.errors import CLK_ERROR, DEL_ERROR, check_code
from config.config_scripts.generate_inputs import gen_in
import config.config_scripts.global_vars as gv

# prepend libs to src file if not already present
def insert_libs(module):
    libs =  '`include "./libs/primitives.v"\n'
    libs += '`include "./libs/sky130_fd_sc_hd.v"\n' 
    libs += '`timescale 1ns / 1fs\n\n'

    m = "./scripts/verilog/src/" + module + ".v"
    m_new = "./scripts/verilog/src/" + module + "_new.v"

    with open(m, "r") as old:
        if old.readline().startswith('`include "./libs/primitives.v"'):
            warnings.warn("Libraries are already inserted in src. Step skipped.")
            return 0

    with open(m, "r") as old:
        with open(m_new, "w") as new:
            new.write(libs)
            for line in old:
                new.write(line)

    os.remove(m)
    os.rename(m_new, m)
    return 1

# auxiliary function reading to help reading the configuration file
def read_del(line):
    return line.split()[1], line.split()[2]

def create_conf_file_v(rand_del, file):
    in_del = dict()
    gate_del = dict()
    clk = 'y'
    period = 0

    # reads the configuration file and initializes all needed values
    with open(file) as conf:
        for line in conf:
            if line.startswith("sim"):
                gv.new_simulations(int(line.split()[1]))
            
            elif line.startswith("full"):
                f = line.split()[1]
                if f == 'n':
                    gv.new_full('n')

            elif line.startswith("clk"):
                clk = line.split()[1]

            elif line.startswith("period"):
                period = int(line.split()[1])

            elif line.startswith("cycles"):
                cycles = int(line.split()[1])

            elif line.startswith("in_size"):
                gv.new_in_size(int(line.split()[1]))

            elif line.startswith("rand_size"):
                gv.new_rand_size(int(line.split()[1]))

            elif line.startswith("out_size"):
                gv.new_out_size(int(line.split()[1]))

            elif line.startswith("input"):
                data = read_del(line)
                in_del[data[0]] = data[1]

            elif line.startswith("gate"):
                data = read_del(line)
                gate_del[data[0]] = data[1]

    if gv.simulations == 0:
        gv.new_simulations(len(in_del)**2)

    if clk == 0:
        check_code(CLK_ERROR)

    if (gv.in_size + gv.rand_size) != len(in_del):
        check_code(DEL_ERROR)

    # uses the values read before to write the verilog configuration file
    # containing all the definitions needed for the simulations
    return write_config_v(rand_del, in_del, gate_del, gv.simulations, clk, period, cycles, gv.in_size, gv.rand_size, gv.out_size)

def write_config_v(rand_del, in_del, gate_del, sim, clk, period, cycles, in_size, rand_size, out_size):
    in_delays = list()
    gate_delays = list()

    file = "./tmp/config/config.v"
    with open(file, "a") as conf:
        conf.truncate(0)

        # write needed defines on the config.v file
        r = int(math.sqrt(sim))
        conf.write("`define SIM " + str(r) + "\n")
        if clk == 'y':
            conf.write("`define CLK\n")
        conf.write("`define CLK_PERIOD " + str(period) + "\n")
        conf.write("`define IN_SIZE " + str(in_size) + "\n")
        conf.write("`define RAND_SIZE " + str(rand_size) + "\n")
        max_in = rand_size + in_size
        conf.write("`define MAX_IN " + str(max_in) + "\n")
        conf.write("`define OUT_SIZE " + str(out_size) + "\n")
        conf.write("`define CYCLES " + str(cycles) + "\n")

        conf.write("\n")

        # if rand_del is set to 1 then the delay values are generated randomly
        # in a range from 0 to 1

        # section of the config.v file containing the gate delays
        conf.write("`ifdef DEL\n")
        if not rand_del:    
            for i in gate_del:
                gate_delays.append(i + " " + gate_del[i])
                string = "  `define " + i + " #" + gate_del[i] + "\n"
                conf.write(string)
        elif rand_del:
            for i in gate_del:
                delay = random()
                gate_delays.append(i + " %.2f" % delay)
                string = "  `define " + i + " #" + str(delay) + "\n"
                conf.write(string)
        conf.write("`else\n")
        for i in gate_del:
            string = "  `define " + i + " #0\n"
            conf.write(string)
        conf.write("`endif\n")

        conf.write("\n")

        # section of the config.v file containing the input delays
        conf.write("`ifdef IN_DEL\n")
        if not rand_del:
            for i in in_del:
                in_delays.append(i + " " + in_del[i])
                string = "  `define " + i + " #" + in_del[i] + "\n"
                conf.write(string)
        elif rand_del:
            for i in in_del:
                delay = random()
                in_delays.append(i + " %.2f" % delay)
                string = "  `define " + i + " #" + str(delay) + "\n"
                conf.write(string)

        conf.write("`else\n")
        for i in in_del:
            string = "  `define " + i + " #0\n"
            conf.write(string)
        conf.write("`endif\n")

    return in_delays, gate_delays


def config(rand_del, conf_file):
    # the configuration file is read and the config.v file generated
    in_delays, gate_delays = create_conf_file_v(rand_del, conf_file)

    # based on the full parameter of the configuration file the inputs are generated
    gen_in()

    return in_delays, gate_delays