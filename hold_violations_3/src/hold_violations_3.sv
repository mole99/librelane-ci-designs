module hold_violations_3 (
    input  clk_i,
    input  rst_ni,

    input  shift_i,
    output shift_o
);

    logic [2:0] data_o;

    flipflop my_ff_1 (
      .clk_i  (clk_i),
      
      .data_i (shift_i),
      .data_o (data_o[0])
    );

    flipflop my_ff_2 (
      .clk_i  (clk_i),
      
      .data_i (data_o[0]),
      .data_o (data_o[1])
    );

    flipflop my_ff_3 (
      .clk_i  (clk_i),
      
      .data_i (data_o[1]),
      .data_o (data_o[2])
    );

    flipflop my_ff_4 (
      .clk_i  (clk_i),
      
      .data_i (data_o[2]),
      .data_o (shift_o)
    );

endmodule
