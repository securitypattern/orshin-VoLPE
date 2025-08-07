//=================================================
// Copyright (c) 2025, Security Pattern
// All rights reserved.
//
//    This file is part of: Side-channel leakages analysis with VoLPE.
//
//    SPDX-License-Identifier: MIT 
//=================================================

`include "./tmp/verilog/interface/interface.v"
`include "./tmp/config/config.v"

`timescale 1ns/1fs
`define NULL 0

module tb;

reg [`MAX_IN-1:0] in;
reg clk;

initial clk = 0;
always #(`CLK_PERIOD / 2) clk = ~clk;

wire [`OUT_SIZE-1:0] out;

interface uut(
	.clk(clk),
    .in(in), .out(out)
	);

integer i;
integer j;
integer sim;
integer inputs;
reg [`RAND_SIZE-1:0] randoms;
reg [`IN_SIZE-1:0] pre_data;
reg [`IN_SIZE-1:0] post_data;

integer scan_file;
integer check;

// simulation	
initial begin

	$dumpfile("./tmp/verilog/vcd/correlation.vcd");
	$dumpvars(0, tb);

    randoms = 63;//$urandom;
	sim = 0;

    inputs = $fopen("./tmp/config/inputs.dat", "r");
    if (inputs == `NULL) begin
        $display("inputs.dat handle was NULL");
        $finish;
    end 
    else begin
        $monitor("out: %b", out);
        for (i = 0; i < `SIM; i++) begin
			for (j = 0; j < `SIM; j++) begin 
                if (!$feof(inputs)) begin
                    scan_file = $fscanf(inputs, "%d\n%d\n", pre_data, post_data);
                   
                    // here i have read the inputs input
                    in = {randoms, pre_data}; #(`CLK_PERIOD * `CYCLES);

                    $write("BEGIN SIM %d\n", sim);
                    $write("state %b\n", out);

                    in = {randoms, post_data}; #(`CLK_PERIOD * `CYCLES); 

                    $write("END\n");
                    sim++;
                end
            end
        end
    end

	$fclose(inputs);

	$finish;
end

endmodule  