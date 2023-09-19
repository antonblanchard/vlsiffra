module and2( A1, A2, Z );
	input A1, A2;
	output Z;

        and MGM_BG_0( Z, A1, A2 );
endmodule

module xor2( A2, A1, Z );
	input A1, A2;
	output Z;

        wire A2_inv_for_xor2;
        not MGM_BG_0( A2_inv_for_xor2, A2 );

        wire Z_row1;
        and MGM_BG( Z_row1, A2_inv_for_xor2, A1 );

        wire A1_inv_for_xor2;
        not MGM_BG_2( A1_inv_for_xor2, A1 );

        wire Z_row2;
        and MGM_BG_3( Z_row2, A1_inv_for_xor2, A2 );
        or MGM_BG_4( Z, Z_row1, Z_row2 );

endmodule

module inv( I, ZN );
	input I;
	output ZN;

        not MGM_BG_0( ZN, I );
endmodule

module addf( S, A, CI, B, CO );
	input A, B, CI;
	output CO, S;

        wire CO_row1;
        and MGM_BG_0( CO_row1, A, B );

        wire CO_row2;
        and MGM_BG( CO_row2, A, CI );

        wire CO_row3;
        and MGM_BG_2( CO_row3, B, CI );
        or MGM_BG_3( CO, CO_row1, CO_row2, CO_row3 );

        wire S_row1;
        and MGM_BG_4( S_row1, A, B, CI );

        wire B_inv_for_addf;
        not MGM_BG_5( B_inv_for_addf, B );

        wire CI_inv_for_addf;
        not MGM_BG_6( CI_inv_for_addf, CI );

        wire S_row2;
        and MGM_BG_7( S_row2, B_inv_for_addf, CI_inv_for_addf, A );

        wire A_inv_for_addf;
        not MGM_BG_8( A_inv_for_addf, A );

        wire S_row3;
        and MGM_BG_9( S_row3, A_inv_for_addf, CI_inv_for_addf, B );

        wire S_row4;
        and MGM_BG0( S_row4, A_inv_for_addf, B_inv_for_addf, CI );
        or MGM_BG1( S, S_row1, S_row2, S_row3, S_row4 );
endmodule

module addh( CO, A, B, S );
	input A, B;
	output CO, S;

        and MGM_BG_0( CO, A, B );

        wire B_inv_for_addh;
        not MGM_BG( B_inv_for_addh, B );

        wire S_row1;
        and MGM_BG_2( S_row1, B_inv_for_addh, A );

        wire A_inv_for_addh;
        not MGM_BG_3( A_inv_for_addh, A );

        wire S_row2;
        and MGM_BG_4( S_row2, A_inv_for_addh, B );
        or MGM_BG_5( S, S_row1, S_row2 );
endmodule

// FIXME: Convert to aoi21
module aoi21( A2, ZN, A1, B );
	input A1, A2, B;
	output ZN;

        wire A1_inv_for_aoi21;
        not MGM_BG_0( A1_inv_for_aoi21, A1 );

        wire B_inv_for_aoi21;
        not MGM_BG( B_inv_for_aoi21, B );

        wire ZN_row1;
        and MGM_BG_2( ZN_row1, A1_inv_for_aoi21, B_inv_for_aoi21 );

        wire A2_inv_for_aoi21;
        not MGM_BG_3( A2_inv_for_aoi21, A2 );

        wire ZN_row2;
        and MGM_BG_4( ZN_row2, A2_inv_for_aoi21, B_inv_for_aoi21 );
        or MGM_BG_5( ZN, ZN_row1, ZN_row2 );
endmodule

// FIXME: Convert to ao22
module aoi22( B2, B1, ZN, A1, A2 );
	input A1, A2, B1, B2;
	output ZN;

        wire A1_inv_for_aoi22;
        not MGM_BG_0( A1_inv_for_aoi22, A1 );

        wire B1_inv_for_aoi22;
        not MGM_BG( B1_inv_for_aoi22, B1 );

        wire ZN_row1;
        and MGM_BG_2( ZN_row1, A1_inv_for_aoi22, B1_inv_for_aoi22 );

        wire B2_inv_for_aoi22;
        not MGM_BG_3( B2_inv_for_aoi22, B2 );

        wire ZN_row2;
        and MGM_BG_4( ZN_row2, A1_inv_for_aoi22, B2_inv_for_aoi22 );

        wire A2_inv_for_aoi22;
        not MGM_BG_5( A2_inv_for_aoi22, A2 );

        wire ZN_row3;
        and MGM_BG_6( ZN_row3, A2_inv_for_aoi22, B1_inv_for_aoi22 );

        wire ZN_row4;
        and MGM_BG_7( ZN_row4, A2_inv_for_aoi22, B2_inv_for_aoi22 );
        or MGM_BG_8( ZN, ZN_row1, ZN_row2, ZN_row3, ZN_row4 );
endmodule

module oai33( B3, B2, B1, ZN, A1, A2, A3 );
	input A1, A2, A3, B1, B2, B3;
	output ZN;

        wire A1_inv_for_oai33;
        not MGM_BG_0( A1_inv_for_oai33, A1 );

        wire A2_inv_for_oai33;
        not MGM_BG( A2_inv_for_oai33, A2 );

        wire A3_inv_for_oai33;
        not MGM_BG_2( A3_inv_for_oai33, A3 );

        wire ZN_row1;
        and MGM_BG_3( ZN_row1, A1_inv_for_oai33, A2_inv_for_oai33, A3_inv_for_oai33 );

        wire B1_inv_for_oai33;
        not MGM_BG_4( B1_inv_for_oai33, B1 );

        wire B2_inv_for_oai33;
        not MGM_BG_5( B2_inv_for_oai33, B2 );

        wire B3_inv_for_oai33;
        not MGM_BG_6( B3_inv_for_oai33, B3 );

        wire ZN_row2;
        and MGM_BG_7( ZN_row2, B1_inv_for_oai33, B2_inv_for_oai33, B3_inv_for_oai33 );
        or MGM_BG_8( ZN, ZN_row1, ZN_row2 );
endmodule
