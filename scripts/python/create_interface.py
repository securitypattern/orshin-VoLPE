#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

from scripts.python.errors import del_error
import config.config_scripts.global_vars as gv

# auxiliary function used to read the name of a delay from the configuration file
def read_del_name(line):
    return line.split()[1]

# creates the general interface taking the values from the configuration file
# permits to automatically execute every gadget with a specific structure
#   -> adds the necessary abstraction level
def create_if(module_name, conf_file):
    fn = "./tmp/verilog/interface/interface.v"
    with open(fn, "w") as interface:
        interface.write('`include "./scripts/verilog/src/' + module_name + '.v"\n')
        interface.write('`include "./tmp/config/config.v"\n\n')
        interface.write('`timescale 1ns/1fs\n\n')
        interface.write('module interface(clk, in, out);\n\n')
        interface.write('\tinput clk;\n')
        interface.write('\tinput [`MAX_IN-1:0] in;\n\n')
        interface.write('\toutput [`OUT_SIZE-1:0] out;\n\n')
        interface.write('\twire [`MAX_IN-1:0] in_del;\n\n')

        # loop to insert delays in inputs
        with open(conf_file, "r") as conf:
            d = gv.in_size + gv.rand_size
            for line in conf:
                if line.startswith("in_name"):
                    in_name = line.split()[1]
                if line.startswith("out_name"):
                    out_name = line.split()[1]
                if line.startswith("input"):
                    d -= 1
                    if d<0:
                        del_error()
                    interface.write('\tassign `' + read_del_name(line) + ' in_del[' + str(d) + '] = in[' + str(d) + '];\n')

        interface.write('\n\t`ifdef CLK\n')
        interface.write('\t\t' + module_name + ' test(.clk(clk), .' + in_name + '(in_del), .' + out_name + '(out));\n')
        interface.write('\t`else\n')
        interface.write('\t\t' + module_name + ' test(.' + in_name + '(in_del), .' + out_name + '(out));\n')
        interface.write('\t`endif\n\n')
        
        
        interface.write('endmodule\n')