# 2 cycle 64 bit multiply-adder (`64bit * 64bit + 128bit -> 128bit`)

Generate the multiplier with:

```
vlsi-multiplier --bits=64 --multiply-add --algorithm=hancarlson --tech=asap7 --register-post-ppg --output=multiply_adder.v
```

Assuming you have setup OpenROAD-flow-scripts, do the following:

```
cd OpenROAD-flow-scripts/flow

make DESIGN_CONFIG=/path/to/vlsiffra/openroad/64bit_2cycle_asap7_multiply_adder/config.mk
```
