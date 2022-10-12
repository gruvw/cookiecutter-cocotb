import pathlib
from rich import print
from cocotb.runner import get_runner
import importlib.util
import sys


def assert_log(expected, actual, name="Assert error"):
    if expected != actual:
        s_expected, s_actual = str(expected), str(actual)
        padding = max(len(s_expected), len(s_actual))
        msg = f"[red]{name} error:\nExpected: {s_expected:>{padding}}\nActual:   {s_actual:>{padding}}"
        print(msg)
        exit()


def _load_module(file):
    spec = importlib.util.spec_from_file_location(file.stem, file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[file.stem] = module
    spec.loader.exec_module(module)
    return module


def test_runner():
    path = pathlib.Path(__file__).parent.resolve()
    directories = ("entities", "architectures", "packages", "vhdl")
    paths = [path.parent / directory for directory in directories]

    vhdl_sources = [file for files in (p.glob("**/*.vhd") for p in paths) for file in files]
    build_params = dict(
        vhdl_sources=vhdl_sources,
        build_dir=path / "sim_build",
    )
    test_params = lambda name: dict(
        extra_args=[
            f"--vcd=waves_{name}.vcd",
            "--ieee-asserts=disable"
        ]
    )

    sys.path.insert(1, str(path / "tests"))
    python_tests = [file for file in path.glob("tests/test_*.py")]

    runner = get_runner("{{ cookiecutter.sim }}")()

    print("[yellow reverse]BUILDING & TESTING VHDL...")
    for python_test in python_tests:
        module = _load_module(python_test)
        if isinstance(module.__toplevel__, str):
            toplevels = [module.__toplevel__]
        else:
            toplevels = module.__toplevel__
        for toplevel in toplevels:
            s_toplevel = f"[bold]{toplevel}[/bold]"
            print(f"[yellow]Building {s_toplevel}...")
            runner.build(toplevel=toplevel, **build_params)
            print(f"[green]Successfully built {s_toplevel}.")
            print(f"[yellow]Testing {s_toplevel}...", "yellow")
            runner.test(
                toplevel=toplevel,
                py_module=module.__name__,
                **test_params(toplevel)
            )
            print(f"[green]Successfully passed {s_toplevel} tests :)")
    print(f"[green reverse]FINISHED TESTING")


if __name__ == "__main__":
    # make -C {{ cookiecutter.project_name }}/
    test_runner()
