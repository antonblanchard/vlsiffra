# 4 cycle 32 bit multiplier (`32bit * 32bit -> 64bit`)

Generate the multiplier with:

```
vlsi-multiplier --bits=32 --algorithm=koggestone --tech=asap7 --register-post-ppa --register-post-ppg --register-output --output=multiplier.v
```

Assuming you have setup OpenROAD-flow-scripts, do the following:

```
cd OpenROAD-flow-scripts/flow

make DESIGN_CONFIG=/path/to/vlsi-arithmetic/openroad/32bit_4cycle_asap7_multiplier/config.mk
```
