# Makefile

# defaults
SIM ?= {{cookiecutter.sim}}
TOPLEVEL_LANG ?= vhdl

# VHDL_SOURCES += $(PWD)/../entities/*
# VHDL_SOURCES += $(PWD)/../architectures/*
# VHDL_SOURCES += $(PWD)/../packages/*
# VHDL_SOURCES += $(PWD)/../vhdl/*

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = {{cookiecutter.vhdl_top_level}}

# MODULE is the basename of the Python test file
MODULE = {{cookiecutter.python_test_name}}

SIM_ARGS=--vcd={{cookiecutter.waves_output_name}}.vcd --ieee-asserts=disable

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
