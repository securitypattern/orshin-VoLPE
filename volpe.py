#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import time
import sys
from datetime import datetime
import threading

from scripts.python.corr_matrix import corr_matrix

fin = threading.Event()

# help function printing all possible arguments
def help():
    print(
        "python3 corr_matrix.p [options]\n" + 
        "possible options:\n" + 
        "-h:    display help message\n\n" + 
        "-m:    define module to be simulated (mandatory)\n\n" +
        "-c:    define configuration file to be used (mandatory)\n\n" +
        "-s:    give name to the spreadsheet where the results are saved\n\n" +
        "-o:    if set also the correlation with the outputs is calculated\n\n" +
        "-i:    has to be set the first time when executing with a new src file.\n" + 
        "       The needed libraries are inserted in the src file.\n" +
        "-r:    input and gate delays have to be generated randomically.\n"
        "-e:    number of times the tool has to be executed in case of random delays.\n" 
    )

# auxiliary function to check time taken for the computations
def done_in(start_time):
    elapsed_time = "{:.4f}".format(time.time() - start_time)
    print("Done in %s seconds\n\n" % elapsed_time)

def print_symbol():
    print(
        "\nWelcome to\n" + 
        "___        ___         __        ________  ________ \n" +
        "\  \      /  /        |  |      |   __   ||   _____|\n" +
        " \  \    /  /________ |  |      |  |  |  ||  |____  \n" +
        "  \  \  /  /|   __   ||  |      |  |__|  ||   ____| \n" + 
        "   \  \/  / |  |  |  ||  |      |   _____||  |      \n" +
        "    \    /  |  |__|  ||  |_____ |  |      |  |_____ \n" +
        "     \__/   |________||________||__|      |________|\n"
    )
    return

def calculating():
    print("Calculating correlations. This may take a few minutes.")
    while True:
        if fin.is_set():
            break
        sys.stdout.write("\rCalculating \\")
        time.sleep(0.5)
        sys.stdout.flush()
        sys.stdout.write("\rCalculating |")
        time.sleep(0.5)
        sys.stdout.flush()
        sys.stdout.write("\rCalculating /")
        time.sleep(0.5)
        sys.stdout.flush()
        sys.stdout.write("\rCalculating -")
        time.sleep(0.5)
        sys.stdout.flush()

    print("\rCalculations finished")

if __name__ == "__main__":

    print_symbol()

    # takes as inputs from the user:
    #   - the name of the gadget present in the src folder to simulate
    #   - the configuration file corresponding to the gadget that needs to be simulated
    #   - the name that the spreadsheet containing the results will get

    arg = sys.argv
    module = None
    conf_file = None
    spreadsheet = "result_" + datetime.now().strftime("%d-%m-%Y_%H:%M")
    out_corr = 0
    init_src = 0
    executions = 1
    rand = 0

    for i in range(1, len(arg)):
        if(arg[i] == "-m"):
            try:
                module = arg[i+1]
            except IndexError:
                raise RuntimeError("Module argument empty")
        if(arg[i] == "-c"):
            try: 
                conf_file = "./config/" + arg[i+1]
            except IndexError:
                raise RuntimeError("Configuration file argument empty")   
        if(arg[i] == "-s"):
            try:
                spreadsheet = arg[i+1]
            except IndexError:
                print("No spreadsheet name was set.\n Default name used.")
        if(arg[i] == "-o"):
            out_corr = 1
        if(arg[i] == "-i"):
            init_src = 1
        if(arg[i] == "-r"):
            rand = 1
        if(arg[i] == "-e"):
            try:
                executions = int(arg[i+1])
            except IndexError:
                raise RuntimeError("No number of executions given")

        if(arg[i] == "-h"):
            help()
            exit(0)
    
    if module is None:
        raise RuntimeError("Module argument empty")

    if conf_file is None:
        raise RuntimeError("Configuration file argument empty")

    if(executions == 1):
        start_time = time.time()

        progress_thread = threading.Thread(target=calculating, name="Progress")
        progress_thread.start()

        data, in_delays, gate_delays = corr_matrix(init_src, module, conf_file, out_corr, spreadsheet, rand)

        fin.set()
        progress_thread.join()

        print("The resulting correlations are:")
        print(data)
        print("Detailed results saved in " + spreadsheet + ".")

        done_in(start_time)

    else:
        for i in range(executions):
            start_time = time.time()
            fin.clear()

            progress_thread = threading.Thread(target=calculating, name="Progress"+str(i))
            progress_thread.start()

            spreadsheet_run = spreadsheet + "_run_" + str(i)
            data, in_delays, gate_delays = corr_matrix(init_src, module, conf_file, out_corr, spreadsheet_run, rand)

            fin.set()
            progress_thread.join()

            print("The resulting correlations for run " + str(i) + " are:")
            print(data)
            print("Detailed results saved in " + spreadsheet_run + ".")        

            done_in(start_time)

    