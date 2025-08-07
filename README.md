# Side-channel leakages analysis with VoLPE

We developed a tool called VoLPE, designed to quantify the power consumption leakage of a circuit by analyzing the toggle activity observed during its simulation. For further information, refer to Deliverable D3.3 of the ORSHIN project.
We included in the repository an example; you can find a [verilog description of the s-box of AES](scripts/verilog/src/aes_sbox_v3.v), a [configuration file](config/config_aes_sbox_v3.conf) and [some results](spreadsheets/aes_v3_30run/) running VoLPE on it.

<!-- # Table Of Contents
- [Table Of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [corr_matrix.py Architecture](#corr_matrixpy-architecture)
- [Running corr_matrix.py](#running-corr_matrixpy)
  - [Synthesize circuit using OpenLane](#synthesize-circuit-using-openlane)
  - [Save synthesized circuit file](#save-synthesized-circuit-file)
  - [Generate configuration file](#generate-configuration-file)
  - [Run corr_matrix.py](#run-corr_matrixpy)
  - [Selection Functions and Consume Models](#selection-functions-and-consume-models)
  - [VoLPE Output](#volpe-output) -->

## Prerequisites
- [OpenLane](https://github.com/The-OpenROAD-Project/OpenLane)
- [Python 3](https://www.python.org/downloads/)
- [Icarus Verilog 11](https://iverilog.fandom.com/wiki/Installation_Guide)
- Unix like System (programm runs a bash script)

Circuit synthesis is performed using the SkyWater [SKY130 PDK technology library](https://skywater-pdk.readthedocs.io/en/main/contents/libraries.html).

## corr_matrix.py Architecture
<!-- <table>
   <tr>
    <td  align="center"><img src="./img/architecture.png" ></td>
  </tr>
</table> -->

To simulate a circuit using corr_matrix.py, you begin with a high-level description of the design. This description must first be synthesized using OpenLane. Once synthesized, the circuit—along with a configuration file (explained in more detail [here](#generate-configuration-file))—is provided as input to corr_matrix.py. The simulation is then carried out via [sim.sh](correlations/scripts/bash/sim.sh), and the results are saved in a spreadsheet (see [here](#corrmatrixpy-output) for further details). The diagram below illustrates the logical relationships between the components of this project, without representing their progression over time.

## Running corr_matrix.py
Steps to run the code:
### Synthesize circuit using OpenLane
Create a directory within OpenLane to store all your circuit designs, and place your circuit code inside this directory. Make sure the filename matches the module name used in the circuit description:
```
cd OpenLane
mkdir my_designs
cd my_designs
cp path/to/<design>.v .
```
Create the folder that is going to contain the new design. This folder has to have the same name as the circuit file and the main module of that circuit:
```
cd OpenLane/designs
mkdir design
```
In "OpenLane", start the docker container: 
```
make mount
```
Create the folder containig your circuit src and configuration file in the "design" folder:
```
flow.tcl -design <design> -src my_designs/<design>.v -init_design_config -add_to_designs
```
After modifying ./OpenLane/designs/circuit/config.json, make sure that the clock name in the file is the same used in the design.v file.
Synthesize the circuit.
With `-tag` you can specify a new name for each run.
```
flow.tcl -design <design> -tag <tag>
```
The synthesized circuit can be found in 
```
./OpenLane/designs/design/runs/tag/results/final/verilog/gl/design.v
```

### Save synthesized circuit file
Insert the synthesized circuit file recieved from [OpenLane](https://github.com/The-OpenROAD-Project/OpenLane) in the [src](correlations/scripts/verilog/src/) folder.

### Generate configuration file
Create the config.conf file for the circuit to be simulated, using the provided template as a guide:
| Argument | Description |
| - | - |
| `sim` | number of simulations to run |
| `full` | y for full simulations and n for randomly generated inputs |
| `clk` | y if simulated circuit needs a clock and n if it doesn't |
| `period` | clock period |
| `cycles` | clock cicles the circuit need to finish calculations |
| `in_size` | number of inputs (inputs + randoms) |
| `in_name` | name of the input ports of the circuit |
| `rand_size` | number of randoms |
| `out_size` | number of oututs |
| `out_name` | name of the output ports of the circuit |
| `input <input_name>` | delay for input_name |
| `gate <gate_name>` | delay for gate_name |

Here an example of a config.conf file:
```
sim: 576
full: n
clk: y
period: 5
cicles: 2
in_size: 6
in_name: in
rand_size: 2
out_size: 4
out_name: out

input a0     0.02
input a1     0.04
input b0     0.45
input b1     0.22
input rand0    0.00
input rand1    0.00

gate XNOR_DELAY   0.10
gate NAND_DELAY   0.20
gate XOR_DELAY    0.50
gate AND_DELAY    0.30
gate OR_DELAY     0.40
```
### Run corr_matrix.py
Run corr_matrix.py with the following command:
`python3 volpe.py -m module -c config.conf`
| Argument | Description |
| - | - |
| `-m` | Name of the circuit to be simulated (without .v). |
| `-c` | Configuration file to be used (from "config" folder). |
| `-i` | Option to intialize the src file during the first run. |

Some optional arguments are:
| Argument | Description |
| - | - |
| `-h` | Print out a help screen with all the possible arguments. |
| `-s` | Name of the spreadsheet where the results are saved. Default name of the spreadsheet is `result_dd-mm-YY_H:M`. |
| `-r` | When this option is enabled, input and gate delays are randomly generated within the range of 0 to 1. |
| `-e` | Number of times the correlation has to be executed. |
| `-o` | Calculate the correlation also with the outputs of the circuit. A software simulation of the circuit is needed. Specify the behaviour of the circuit in the [output_sim.py](correlations/scripts/python/output_sim.py) script. |

### Selection Functions and Consume Models
Default selection functions and consume models are given in the code. If specific functions are needed, personal functions can be inserted in the [selection_functions.py](correlations/scripts/python/selection_functions.py) and [consume_models.py](correlations/scripts/python/consume_models.py) scripts respectively.

### VoLPE Output
The results are located in the [spreadsheets](correlations/spreadsheets/) folder.
The first sheet presents the calculated correlation matrix, while the remaining sheets display histograms showing the number of toggles from simulations with no delays, gate delays, and both gate and input delays, respectively.
