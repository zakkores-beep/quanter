"""Local judge for the coding problems.

    python judge.py --list               # all problems and your progress
    python judge.py 7                    # judge work/07_*.py (created from the starter on first use)
    python judge.py 7 --show             # also reveal failing inputs, expected and actual output
    python judge.py 7 --file my.py       # judge another file
    python judge.py --mock               # 1 easy + 1 medium problem, 30-minute timer

    --tl-scale 1.5   multiply all time limits (if your laptop is slow)
"""
import argparse
import datetime
import json
import os
import random
import shutil
import subprocess
import sys
import threading
import time

from common import PROBLEMS, ROOT, TESTS, WORK, canon, keys, load_spec, resolve, sha

RUNNER = os.path.join(ROOT, "runner.py")
PROGRESS = os.path.join(WORK, "progress.json")
MOCK_HISTORY = os.path.join(WORK, "mock_history.json")


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=1)


def short(x, n=400):
    s = repr(x)
    return s if len(s) <= n else s[:n] + " ... (%d chars)" % len(s)


def run_one(sol, key, test, scale=1.0, func=None):
    """Run one test in a fresh process. Returns a dict with 'verdict' in PASS/WA/TLE/RE/ERR."""
    tl = test["time_limit"] * scale
    cmd = [sys.executable, RUNNER, sol, key] + ([func] if func else [])
    try:
        p = subprocess.run(cmd, input=json.dumps(test["input"]), capture_output=True, text=True,
                           timeout=tl + 3)
    except subprocess.TimeoutExpired:
        return {"verdict": "TLE", "time": None, "detail": "killed after %.1fs" % (tl + 3)}
    try:
        reply = json.loads(p.stdout)
    except ValueError:
        return {"verdict": "RE", "time": None,
                "detail": (p.stderr.strip() or "process crashed (exit code %s)" % p.returncode)[-1500:]}
    if not reply["ok"]:
        return {"verdict": "RE", "time": None, "detail": reply["error"], "stderr": p.stderr}
    if "input_sha" in reply and reply["input_sha"] != test["input_sha"]:
        return {"verdict": "ERR", "time": None,
                "detail": "perf input differs from the one used at build time (Python version?)"}
    got = reply["result"]
    if "expected_sha" in test:
        ok = sha(got) == test["expected_sha"]
    else:
        ok = canon(got) == canon(test["expected"])
    verdict = "PASS" if ok else "WA"
    if reply["time"] > tl:
        verdict = "TLE"
    return {"verdict": verdict, "time": reply["time"], "got": got, "stderr": p.stderr}


def judge(key, sol, show=False, scale=1.0, quiet=False, hint=True):
    tests = load_json(os.path.join(TESTS, key + ".json"), None)
    if tests is None:
        raise SystemExit("No tests for %s - run python build.py" % key)
    if not quiet:
        print("\n%s   (%s)" % (key, os.path.relpath(sol)))
    passed = 0
    for t in tests["tests"]:
        r = run_one(sol, key, t, scale)
        passed += r["verdict"] == "PASS"
        tl = t["time_limit"] * scale
        timing = "%.3fs" % r["time"] if r["time"] is not None else ">%.1fs" % tl
        if quiet:
            continue
        print("  %-8s %-4s  %s" % (t["name"], r["verdict"], timing))
        if r["verdict"] == "RE":
            print(indent(r["detail"]))
        elif r["verdict"] == "ERR":
            print("    " + r["detail"])
        if show and r["verdict"] in ("WA", "TLE"):
            if t["name"] == "perf":
                print("    input:    large generated input (%s)" % t["size"])
                print("    expected: (hidden - too large)   got: %s" % short(r.get("got"), 200))
            else:
                print("    input:    " + short(t["input"]))
                print("    expected: " + short(t["expected"]))
                if "got" in r:
                    print("    got:      " + short(r["got"]))
        if show and r.get("stderr", "").strip() and r["verdict"] != "PASS":
            print("    your print output:\n" + indent(r["stderr"][-800:]))
    total = len(tests["tests"])
    if not quiet:
        print("Result: %d/%d passed%s" % (passed, total, "  ✔ solved" if passed == total else ""))
        if passed < total and not show and hint:
            print("(hidden inputs stay hidden - rerun with --show to reveal them)")
    return passed, total


def indent(s):
    return "\n".join("    | " + line for line in s.rstrip().splitlines())


def record(key, passed, total):
    prog = load_json(PROGRESS, {})
    p = prog.get(key, {"best": 0, "attempts": 0})
    p["attempts"] += 1
    p["best"] = max(p["best"], passed)
    p["total"] = total
    p["last"] = datetime.datetime.now().isoformat(timespec="minutes")
    prog[key] = p
    save_json(PROGRESS, prog)


def work_file(key, folder=WORK):
    path = os.path.join(folder, key + ".py")
    if not os.path.exists(path):
        os.makedirs(folder, exist_ok=True)
        shutil.copy(os.path.join(PROBLEMS, key, "starter.py"), path)
        return path, True
    return path, False


def solved(p):
    return bool(p) and p["best"] == p["total"]


def cmd_list():
    prog = load_json(PROGRESS, {})
    print("%-3s %-30s %-7s %-18s %s" % ("#", "problem", "level", "topic", "status"))
    for key in keys():
        s = load_spec(key)
        p = prog.get(key)
        status = "-" if not p else ("solved" if solved(p) else "best %d/%d" % (p["best"], p["total"]))
        print("%-3d %-30s %-7s %-18s %s" % (s.ID, s.TITLE[:30], s.LEVEL, s.TOPIC, status))


def cmd_mock(minutes, scale):
    prog = load_json(PROGRESS, {})
    specs = [load_spec(k) for k in keys()]
    picks = []
    for level in ("easy", "medium"):
        pool = [s for s in specs if s.LEVEL == level]
        fresh = [s for s in pool if not solved(prog.get(key_of(s)))]
        picks.append(random.choice(fresh or pool))
    folder = os.path.join(WORK, "mock")
    os.makedirs(folder, exist_ok=True)
    files = []
    print("MOCK - Software Fundamentals: %d minutes, 2 problems. No notes, no AI, no internet.\n" % minutes)
    for s in picks:
        key = key_of(s)
        path = os.path.join(folder, key + ".py")
        shutil.copy(os.path.join(PROBLEMS, key, "starter.py"), path)
        files.append((key, path))
        print("  [%s] %s\n      read:  %s\n      edit:  %s" % (
            s.LEVEL, s.TITLE, os.path.relpath(os.path.join(PROBLEMS, key, "statement.md")), os.path.relpath(path)))
    start = time.time()
    deadline = start + minutes * 60
    lock = threading.Lock()

    def grade(final):
        with lock:
            results = []
            for key, path in files:
                passed, total = judge(key, path, scale=scale, hint=False)
                results.append((key, passed, total))
            if final:
                used = (time.time() - start) / 60
                print("\n=== MOCK RESULT ===  time used: %.1f / %d min" % (used, minutes))
                for key, p, t in results:
                    print("  %-30s %2d/%d" % (key, p, t))
                    record(key, p, t)
                hist = load_json(MOCK_HISTORY, [])
                hist.append({"date": datetime.datetime.now().isoformat(timespec="minutes"),
                             "minutes_used": round(used, 1),
                             "results": [{"key": k, "passed": p, "total": t} for k, p, t in results]})
                save_json(MOCK_HISTORY, hist)
                print("Saved to work/mock_history.json")

    def timer():
        for warn in (15, 5, 1):
            wait = deadline - warn * 60 - time.time()
            if wait > 0:
                time.sleep(wait)
                print("\n*** %d minute%s left ***" % (warn, "" if warn == 1 else "s"))
        time.sleep(max(0, deadline - time.time()))
        print("\n*** TIME UP - auto-submitting ***")
        grade(final=True)
        os._exit(0)

    threading.Thread(target=timer, daemon=True).start()
    print("\nCommands: [Enter] run tests   t = time left   done = submit and finish")
    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            cmd = "done"
        if cmd == "t":
            left = deadline - time.time()
            print("%d:%02d left" % (left // 60, left % 60))
        elif cmd == "done":
            grade(final=True)
            return
        else:
            grade(final=False)


def key_of(spec):
    return [k for k in keys() if int(k.split("_")[0]) == spec.ID][0]


def main():
    ap = argparse.ArgumentParser(description="Local judge (see the docstring at the top of judge.py).")
    ap.add_argument("problem", nargs="?")
    ap.add_argument("--file")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--minutes", type=int, default=30)
    ap.add_argument("--tl-scale", type=float, default=1.0)
    a = ap.parse_args()
    if a.list:
        return cmd_list()
    if a.mock:
        return cmd_mock(a.minutes, a.tl_scale)
    if not a.problem:
        ap.print_help()
        return
    key = resolve(a.problem)
    if a.file:
        sol = a.file
    else:
        sol, created = work_file(key)
        if created:
            print("Created %s from the starter.\nRead  %s\nthen edit the file and run this command again."
                  % (os.path.relpath(sol), os.path.relpath(os.path.join(PROBLEMS, key, "statement.md"))))
            return
    passed, total = judge(key, os.path.abspath(sol), a.show, a.tl_scale)
    if not a.file:
        record(key, passed, total)


if __name__ == "__main__":
    main()
