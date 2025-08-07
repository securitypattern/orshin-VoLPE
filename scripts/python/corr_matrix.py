#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

from scripts.python.excel import write_excel
from scripts.python.simulation import simulate
from scripts.python.cm_hist import create_cm_hist
from config.config_scripts.config import config, insert_libs

def corr_matrix(init_src, module, conf_file, out_corr, spreadsheet, rand):
    # if init_src=1 the libraries are inserted into the src file (for first execution)
    if init_src:
        insert_libs(module)

    # starting from the configuration file global variables are defined
    # and the verilog file with all the needed `define is created
    in_delays, gate_delays = config(rand, conf_file)

    # the gadget passed as parameter is simulated three times:
    #   - 1st simulation: ideal gadget with no delays
    #   - 2nd simulation: the gates of the gadget have a delay in the computation
    #   - 3rd simulation: in addition to the previous delays also the inputs have delays
    # and the results are saved in the logs contained in the logs folder
    vvp_logs = simulate(module, conf_file)

    # the lists containing the number of toggles for the different simulations are created
    # through the selection function and the consume model function (that can be changed by the user)
    # the correlations are calculated between the chosen inputs and the number of toggles
    data = create_cm_hist(vvp_logs, out_corr)

    # the correlation function is printed on terminal as well as saved on the spreadsheet
    write_excel(spreadsheet, data, in_delays, gate_delays)

    return data[0], in_delays, gate_delays


        