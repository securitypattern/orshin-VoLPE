`define SIM 64
`define CLK
`define CLK_PERIOD 5
`define IN_SIZE 6
`define RAND_SIZE 0
`define MAX_IN 6
`define OUT_SIZE 1
`define CYCLES 1

`ifdef DEL
  `define XNOR_DELAY #0.8683539272256258
  `define NAND_DELAY #0.5839721397369196
  `define XOR_DELAY #0.3104966901247589
  `define AND_DELAY #0.8541323506655015
  `define OR_DELAY #0.3089028959220421
  `define NOR_DELAY #0.12574142665264398
`else
  `define XNOR_DELAY #0
  `define NAND_DELAY #0
  `define XOR_DELAY #0
  `define AND_DELAY #0
  `define OR_DELAY #0
  `define NOR_DELAY #0
`endif

`ifdef IN_DEL
  `define a0 #0.3190742456456004
  `define a1 #0.015791209698989395
  `define a2 #0.9498077165989496
  `define a3 #0.4585867730491814
  `define a4 #0.8121529009336889
  `define a5 #0.4994122272888226
`else
  `define a0 #0
  `define a1 #0
  `define a2 #0
  `define a3 #0
  `define a4 #0
  `define a5 #0
`endif
