`include "./scripts/verilog/src/chi_noprot_mod_xor.v"
`include "./tmp/config/config.v"

`timescale 1ns/1fs

module interface(clk, in, out);

	input clk;
	input [`MAX_IN-1:0] in;

	output [`OUT_SIZE-1:0] out;

	wire [`MAX_IN-1:0] in_del;

	assign `a0 in_del[5] = in[5];
	assign `a1 in_del[4] = in[4];
	assign `a2 in_del[3] = in[3];
	assign `a3 in_del[2] = in[2];
	assign `a4 in_del[1] = in[1];
	assign `a5 in_del[0] = in[0];

	`ifdef CLK
		chi_noprot_mod_xor test(.clk(clk), .in(in_del), .out(out));
	`else
		chi_noprot_mod_xor test(.in(in_del), .out(out));
	`endif

endmodule
