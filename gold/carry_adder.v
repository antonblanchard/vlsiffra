module gold_carry_adder
#(
    parameter BITS=64
) (
`ifdef USE_POWER_PINS
    input VPWR,
    input VGND,
`endif
    input [BITS-1:0] a,
    input [BITS-1:0] b,
    input carry_in,
    output [BITS-1:0] o,
    output carry_out
);
    assign {carry_out, o} = a + b + carry_in;
endmodule
