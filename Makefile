check: pythontests verilator formal

.PHONY: venv
venv:
	ci/create_venv.sh

.PHONY: pythontests
pythontests: venv
	ci/pythontests.sh

.PHONY: verilator
verilator: venv
	ci/verilator.sh

.PHONY: formal
formal: venv
	ci/formal.sh
