"""Paths and helpers shared by build.py, judge.py, verify.py and runner.py."""
import hashlib
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(ROOT, "specs")
SOLUTIONS = os.path.join(ROOT, "solutions")
PROBLEMS = os.path.join(ROOT, "problems")
TESTS = os.path.join(ROOT, "tests")
WORK = os.path.join(ROOT, "work")
DEFAULT_TL = 2.0  # seconds per test unless the spec sets TIME_LIMIT for the perf test


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def keys():
    return sorted(f[:-3] for f in os.listdir(SPECS) if f.endswith(".py") and f[0].isdigit())


def load_spec(key):
    return load_module(os.path.join(SPECS, key + ".py"), "spec_" + key)


def solution_path(key):
    return os.path.join(SOLUTIONS, key + ".py")


def resolve(name):
    """Accept '7', '07', 'best_k_window', 'best-k-window' or '07_best_k_window'."""
    ks = keys()
    if name in ks:
        return name
    for k in ks:
        num, slug = k.split("_", 1)
        if (name.isdigit() and int(name) == int(num)) or name.replace("-", "_") == slug:
            return k
    raise SystemExit("Unknown problem %r. Try: python judge.py --list" % name)


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(canon(x).encode()).hexdigest()


def prepare(spec, case):
    """Deep-copy a JSON test case and turn it into keyword arguments."""
    case = json.loads(canon(case))
    return spec.to_args(case) if hasattr(spec, "to_args") else case


def finish(spec, res):
    """Turn a returned value into canonical JSON data for comparison."""
    if hasattr(spec, "from_result"):
        res = spec.from_result(res)
    try:
        res = json.loads(canon(res))
    except (TypeError, ValueError):
        raise TypeError("returned %s, which is not a supported answer type" % type(res).__name__)
    if hasattr(spec, "normalize"):
        res = spec.normalize(res)
    return res


def call(spec, func, case):
    return finish(spec, func(**prepare(spec, case)))
