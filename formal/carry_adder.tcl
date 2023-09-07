yosys -import

read_verilog -defer gold/carry_adder.v
chparam -set BITS $::env(BITS) gold_carry_adder
prep -flatten -top gold_carry_adder
splitnets -ports
design -stash gold

read_verilog $::env(VERILOG) $::env(PROCESS_VERILOG)
prep -flatten -top adder
splitnets -ports
design -stash gate

design -copy-from gold -as gold gold_carry_adder
design -copy-from gate -as gate adder
equiv_make gold gate equiv
prep -flatten -top equiv

opt_clean -purge
#show -prefix equiv-prep -colors 1 -stretch

opt -full
equiv_simple
equiv_induct
equiv_status -assert
