export PLATFORM    = asap7

export DESIGN_NAME = multiplier

export VERILOG_FILES = $(DESIGN_DIR)/multiplier.v
export SDC_FILE      = $(DESIGN_DIR)/constraint.sdc

export PLACE_DENSITY = 0.41

export DIE_AREA = 0 0 45.576 47.79
export CORE_AREA = 0.27 1.35 45.31 46.44

# Tuning
export CTS_BUF_CELL = BUFx8_ASAP7_75t_R

export CELL_PAD_IN_SITES_GLOBAL_PLACEMENT ?= 1
export CELL_PAD_IN_SITES_DETAIL_PLACEMENT ?= 0
