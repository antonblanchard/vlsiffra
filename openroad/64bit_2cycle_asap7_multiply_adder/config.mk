export PLATFORM    = asap7

export DESIGN_NAME = multiply_adder

export VERILOG_FILES = $(DESIGN_DIR)/multiply_adder.v
export SDC_FILE      = $(DESIGN_DIR)/constraint.sdc

export PLACE_DENSITY = 0.67

export DIE_AREA = 0 0 60.588 62.91
export CORE_AREA = 0.27 1.35 60.318 61.56

# Tuning
export CTS_BUF_CELL = BUFx8_ASAP7_75t_R

export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 1
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0
