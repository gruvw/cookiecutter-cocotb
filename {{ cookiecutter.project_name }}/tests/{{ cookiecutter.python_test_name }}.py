import cocotb
from test import assert_log
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from cocotb.triggers import Timer, RisingEdge, FallingEdge


__toplevel__ = "{{ cookiecutter.vhdl_top_level }}"


async def reset(dut):
    await FallingEdge(dut.{{cookiecutter.dut_clock_input}})
    # TODO RESET (default inputs)
    dut.{{cookiecutter.dut_reset_input}}.value = 1
    await RisingEdge(dut.{{cookiecutter.dut_clock_input}})
    await FallingEdge(dut.{{cookiecutter.dut_clock_input}})
    dut.{{cookiecutter.dut_reset_input}}.value = 0


@cocotb.test()
async def test(dut):

    cocotb.start_soon(Clock(dut.{{cookiecutter.dut_clock_input}}, 4, units="ns").start(start_high=False))
    await reset(dut)

    await Timer(2, units="ns")
    assert_log(0, dut.{{cookiecutter.dut_reset_input}}.value)
