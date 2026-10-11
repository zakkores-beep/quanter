"""Generate problems/<key>/{statement.md, starter.py} and tests/<key>.json from
specs/ and solutions/.

Every expected output comes from the reference solution AND must match the
brute-force solution (the single perf test is too big for brute force, so its
expected answer comes from the reference only, which verify.py cross-checks
against brute force on 500+ random inputs).

    python build.py            # all problems
    python build.py 7 12       # some problems
"""
import json
import os
import random
import sys
import time

from common import (DEFAULT_TL, PROBLEMS, TESTS, call, canon, keys, load_module, load_spec,
                    resolve, sha, solution_path)

MIN_TESTS = 15  # including the perf test


def load_pair(key):
    spec = load_spec(key)
    sol = load_module(solution_path(key), "sol_" + key)
    return spec, getattr(sol, spec.FUNC), sol.brute


def require_valid(key, spec, case):
    if not spec.valid(case):
        raise SystemExit("%s: input violates the stated constraints: %s" % (key, canon(case)[:300]))


def checked(key, spec, ref, brute, case):
    require_valid(key, spec, case)
    a = call(spec, ref, case)
    b = call(spec, brute, case)
    if canon(a) != canon(b):
        raise SystemExit("%s: reference and brute force DISAGREE on %s\n  ref=%s\n  brute=%s"
                         % (key, canon(case)[:300], canon(a)[:200], canon(b)[:200]))
    return a


def size_of(case):
    parts = []
    for k, v in case.items():
        if isinstance(v, (list, str)):
            parts.append("%s: %d items" % (k, len(v)))
    return ", ".join(parts)


def make_tests(key):
    spec, ref, brute = load_pair(key)
    rng = random.Random(1000 + spec.ID)
    cases, seen = [], set()

    def add(c):
        if canon(c) not in seen:
            seen.add(canon(c))
            cases.append(c)

    for c in spec.edge_cases():
        add(c)
    n_edge = len(cases)
    tries = 0
    while len(cases) < MIN_TESTS - 1 or len(cases) - n_edge < 6:
        add(spec.random_case(rng))
        tries += 1
        if tries > 5000:
            raise SystemExit("%s: random_case cannot produce enough distinct cases" % key)

    tests = []
    for i, c in enumerate(cases):
        name = "edge-%d" % (i + 1) if i < n_edge else "rand-%d" % (i - n_edge + 1)
        tests.append({"name": name, "input": c, "expected": checked(key, spec, ref, brute, c),
                      "time_limit": DEFAULT_TL})

    seed = 7919 * spec.ID
    big = spec.perf_case(random.Random(seed))
    require_valid(key, spec, big)
    t0 = time.perf_counter()
    expected = call(spec, ref, big)
    ref_time = time.perf_counter() - t0
    tests.append({"name": "perf", "input": {"perf_seed": seed}, "input_sha": sha(big),
                  "expected_sha": sha(expected), "size": size_of(big),
                  "time_limit": getattr(spec, "TIME_LIMIT", DEFAULT_TL)})
    return {"key": key, "tests": tests}, ref_time


def fmt_args(case):
    return ", ".join("%s = %r" % (k, v) for k, v in case.items())


def make_statement(key):
    spec, ref, brute = load_pair(key)
    lines = ["# %d. %s" % (spec.ID, spec.TITLE), "",
             "**Difficulty:** %s · **Topic:** %s" % (spec.LEVEL, spec.TOPIC), "",
             spec.STATEMENT.strip(), "", "## Function", "", "```python", spec.SIGNATURE, "```", "",
             "## Constraints", "", spec.CONSTRAINTS.strip(), "", "## Examples", ""]
    for i, ex in enumerate(spec.EXAMPLES, 1):
        out = checked(key, spec, ref, brute, ex)
        lines += ["**Example %d**" % i, "", "```", "Input:  " + fmt_args(ex), "Output: %r" % (out,),
                  "```", ""]
    lines += ["## Run", "", "```", "python judge.py %d" % spec.ID, "```", ""]
    return "\n".join(lines)


def make_starter(key):
    spec = load_spec(key)
    head = getattr(spec, "IMPORTS", "")
    return (head + "\n\n" if head else "") + spec.SIGNATURE + "\n    # Write your solution here.\n    pass\n"


def main():
    targets = [resolve(a) for a in sys.argv[1:]] or keys()
    os.makedirs(TESTS, exist_ok=True)
    for key in targets:
        d = os.path.join(PROBLEMS, key)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "statement.md"), "w") as f:
            f.write(make_statement(key))
        with open(os.path.join(d, "starter.py"), "w") as f:
            f.write(make_starter(key))
        tests, ref_time = make_tests(key)
        with open(os.path.join(TESTS, key + ".json"), "w") as f:
            json.dump(tests, f, indent=1)
        print("built %-28s %2d tests  (ref perf %.3fs)" % (key, len(tests["tests"]), ref_time))


if __name__ == "__main__":
    main()
