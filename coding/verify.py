"""Verify the coding trainer. Exit code 1 if anything fails.

For every problem:
  1. tests/<key>.json and statement.md are exactly what build.py regenerates now
     (so every stored expected answer and every example was just re-checked
     against BOTH the reference and the brute force);
  2. at least 15 tests, exactly one perf test;
  3. the reference solution passes every test through the real judge
     (separate process, time limits);
  4. brute force agrees with the reference on N random inputs (default 500);
  5. the starter file loads and runs without crashing;
  6. every input (edge, random, examples, perf) satisfies the stated
     constraints (spec.valid), the tests have at least 2 different answers
     (True AND False for yes/no problems), and the reference needs at most
     1/4 of the perf time limit (headroom for slower laptops);
  7. (info) whether brute force is too slow for the perf test - shows the perf
     test actually separates efficient from naive solutions.

    python verify.py                 # everything
    python verify.py 3 7 --n 2000    # some problems, more random checks
    python verify.py --skip-brute-perf
"""
import argparse
import json
import os
import random
import sys

from build import checked, load_pair, make_statement, make_tests
from common import PROBLEMS, TESTS, canon, keys, resolve, solution_path
from judge import run_one


def verify(key, n_random, brute_perf):
    errors, info = [], {}
    spec, ref, brute = load_pair(key)
    with open(os.path.join(TESTS, key + ".json")) as f:
        stored = json.load(f)
    fresh, _ = make_tests(key)
    if canon(stored) != canon(fresh):
        errors.append("stored tests differ from regenerated tests (run build.py)")
    with open(os.path.join(PROBLEMS, key, "statement.md")) as f:
        if f.read() != make_statement(key):
            errors.append("statement.md differs from regenerated statement (run build.py)")
    tests = stored["tests"]
    perf = [t for t in tests if t["name"] == "perf"]
    if len(tests) < 15 or len(perf) != 1:
        errors.append("needs >= 15 tests with exactly one perf test (has %d, perf %d)" % (len(tests), len(perf)))

    answers = [canon(t["expected"]) for t in tests if "expected" in t]
    if len(set(answers)) < 2:
        errors.append("all tests have the same answer")
    if any(a in ("true", "false") for a in answers) and not {"true", "false"} <= set(answers):
        errors.append("yes/no problem but tests do not contain both True and False")
    info["distinct"] = len(set(answers))

    sol = solution_path(key)
    for t in tests:
        r = run_one(sol, key, t)
        if r["verdict"] != "PASS":
            errors.append("reference %s on %s: %s" % (r["verdict"], t["name"], r.get("detail", "")[-300:]))
        if t["name"] == "perf":
            info["ref_perf"] = r["time"]
            info["limit"] = t["time_limit"]
            if r["time"] is not None and r["time"] > t["time_limit"] / 4:
                errors.append("reference perf time %.2fs exceeds 1/4 of the limit" % r["time"])

    rng = random.Random(99991 + spec.ID)
    agree = 0
    for _ in range(n_random):
        case = spec.random_case(rng)
        try:
            checked(key, spec, ref, brute, case)
            agree += 1
        except SystemExit as e:
            errors.append(str(e))
            break
    info["agree"] = agree

    r = run_one(os.path.join(PROBLEMS, key, "starter.py"), key, tests[0])
    if r["verdict"] not in ("WA", "PASS"):
        errors.append("starter crashed: %s" % r.get("detail", "")[-300:])

    if brute_perf and perf:
        info["brute_perf"] = run_one(sol, key, perf[0], func="brute")["verdict"]
    return errors, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("problems", nargs="*")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--skip-brute-perf", action="store_true")
    a = ap.parse_args()
    targets = [resolve(p) for p in a.problems] or keys()
    print("%-26s %5s %8s %10s %10s %10s  %s" % ("problem", "tests", "answers", "brute=ref", "ref perf", "brute perf", "status"))
    failed = 0
    slow_brute = 0
    for key in targets:
        errors, info = verify(key, a.n, not a.skip_brute_perf)
        with open(os.path.join(TESTS, key + ".json")) as f:
            n_tests = len(json.load(f)["tests"])
        bp = info.get("brute_perf", "-")
        slow_brute += bp in ("TLE", "RE")
        ref_perf = "%.2f/%.0fs" % (info["ref_perf"], info["limit"]) if info.get("ref_perf") is not None else "?"
        print("%-26s %5d %8d %6d/%-3d %10s %10s  %s" % (key, n_tests, info.get("distinct", 0), info.get("agree", 0),
                                                        a.n, ref_perf, bp, "OK" if not errors else "FAIL"))
        for e in errors:
            print("    ! " + e)
        failed += bool(errors)
        sys.stdout.flush()
    print("\n%d/%d problems verified, %d failed. Brute force fails the perf test (TLE or recursion crash) in %d/%d problems."
          % (len(targets) - failed, len(targets), failed, slow_brute, len(targets)))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
