import cocotb
import pathlib
from termcolor import colored
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import Timer, RisingEdge, FallingEdge


def assert_log(expected, actual, name=None):
    pref = f"{name} error" if name else "Assert error"
    err_msg = colored(f"{pref} expected {expected}, actual {actual}", "red")
    assert expected == actual, err_msg


async def reset(dut):
    await FallingEdge(dut.{{cookiecutter.dut_clock_input}})
    # TODO RESET (default inputs)
    dut.{{cookiecutter.dut_reset_input}}.value = 1
    await RisingEdge(dut.{{cookiecutter.dut_clock_input}})
    dut.{{cookiecutter.dut_reset_input}}.value = 0
    await RisingEdge(dut.{{cookiecutter.dut_clock_input}})


@cocotb.test()
async def counter_test(dut):

    cocotb.start_soon(Clock(dut.{{cookiecutter.dut_clock_input}}, 4, units="ns").start(start_high=False))
    await reset(dut)

    await Timer(2, units="ns")
    assert_log(0, dut.{{cookiecutter.dut_reset_input}}.value)

    print(colored("Test finished!", "green"))


def test_runner():
    path = pathlib.Path(__file__).parent.resolve()
    directories = ("entities", "architectures", "packages", "vhdl")
    paths = [path.parent / directory for directory in directories]

    vhdl_sources = [file for files in (p.glob("**/*.vhd") for p in paths) for file in files]

    runner = get_runner("{{cookiecutter.sim}}")()
    runner.build(vhdl_sources=vhdl_sources, toplevel="{{cookiecutter.vhdl_top_level}}", build_dir=path / "sim_build")
    runner.test(
        toplevel="{{cookiecutter.vhdl_top_level}}",
        py_module="{{cookiecutter.python_test_name}}",
        extra_args=[
            "--vcd={{cookiecutter.waves_output_name}}.vcd",
            "--ieee-asserts=disable"
        ]
    )


if __name__ == "__main__":
    # make -C cocotb/
    test_runner()
