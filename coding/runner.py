"""Runs ONE test in a fresh process (called by judge.py / verify.py).

    python runner.py <solution.py> <problem_key> [function_name]   < case.json

Prints a JSON reply: {"ok": true, "result": ..., "time": seconds} or
{"ok": false, "error": traceback}. Only the function call itself is timed.
"""
import json
import os
import random
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402


def main():
    sol_path, key = sys.argv[1], sys.argv[2]
    func_name = sys.argv[3] if len(sys.argv) > 3 else None
    case = json.loads(sys.stdin.read())
    real_stdout = sys.stdout
    sys.stdout = sys.stderr  # print() in your solution must not corrupt the reply
    reply = {}
    try:
        spec = common.load_spec(key)
        if "perf_seed" in case:
            case = spec.perf_case(random.Random(case["perf_seed"]))
            reply["input_sha"] = common.sha(case)
        args = common.prepare(spec, case)
        mod = common.load_module(sol_path, "solution")
        name = func_name or spec.FUNC
        func = getattr(mod, name, None)
        if func is None:
            raise AttributeError("function %s() not found in %s" % (name, sol_path))
        t0 = time.perf_counter()
        res = func(**args)
        reply["time"] = time.perf_counter() - t0
        reply["result"] = common.finish(spec, res)
        reply["ok"] = True
    except BaseException:  # RecursionError, SystemExit, ... all count as runtime errors
        reply["ok"] = False
        reply["error"] = traceback.format_exc(limit=-6)
    real_stdout.write(json.dumps(reply))
    real_stdout.flush()


if __name__ == "__main__":
    main()
