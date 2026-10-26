"""Draw the development-case sample and seal the V/N labels (step S2 in README.md).

Usage:
  python3 sample_and_seal.py frame.csv --v-cap 1 --n-count 6 --seed <integer> --out <folder>
  python3 sample_and_seal.py --self-check

frame.csv has one row per eligible audit-scope function, with columns: function_id, file, function, stratum (V or N).
V functions are taken in full if there are at most --v-cap of them, otherwise a simple random sample of --v-cap.
N functions are a simple random sample of --n-count. Each kept function gets its inclusion probability.
The student gets task_list.csv: a shuffled list of codes with file and function, without the stratum.
The labels go to sealed_labels.json, whose SHA-256 is written to seal_hash.txt; record that hash in the timesheet.
"""
import argparse, csv, hashlib, json, os, random, sys, tempfile


def draw(rows, v_cap, n_count, seed):
    rng = random.Random(seed)
    out = []
    for stratum, k in (("V", v_cap), ("N", n_count)):
        pool = sorted((r for r in rows if r["stratum"] == stratum), key=lambda r: r["function_id"])
        take = pool if len(pool) <= k else rng.sample(pool, k)
        out += [dict(r, inclusion_probability=(len(take) / len(pool)) if pool else 0.0) for r in take]
    rng.shuffle(out)
    for i, r in enumerate(out, 1):
        r["code"] = f"F{i:02d}"
    return out


def write(sample, folder, seed):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "task_list.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["code", "file", "function"])
        for r in sample:
            w.writerow([r["code"], r["file"], r["function"]])
    sealed = json.dumps({"seed": seed, "functions": [{k: r[k] for k in ("code", "function_id", "file", "function", "stratum", "inclusion_probability")} for r in sample]}, indent=2, sort_keys=True)
    with open(os.path.join(folder, "sealed_labels.json"), "w") as f:
        f.write(sealed)
    digest = hashlib.sha256(sealed.encode()).hexdigest()
    with open(os.path.join(folder, "seal_hash.txt"), "w") as f:
        f.write(digest + "\n")
    return digest


def self_check():
    rows = [{"function_id": f"v{i}", "file": "A.sol", "function": f"v{i}", "stratum": "V"} for i in range(9)]
    rows += [{"function_id": f"n{i}", "file": "B.sol", "function": f"n{i}", "stratum": "N"} for i in range(30)]
    s = draw(rows, 6, 8, 7)
    assert sum(r["stratum"] == "V" for r in s) == 6 and sum(r["stratum"] == "N" for r in s) == 8
    assert all(abs(r["inclusion_probability"] - (6 / 9 if r["stratum"] == "V" else 8 / 30)) < 1e-12 for r in s)
    assert draw(rows, 6, 8, 7) == s, "same seed must give the same sample"
    small = draw(rows[:2] + rows[9:], 6, 8, 7)
    assert sum(r["stratum"] == "V" for r in small) == 2 and all(r["inclusion_probability"] == 1.0 for r in small if r["stratum"] == "V")
    with tempfile.TemporaryDirectory() as d:
        h = write(s, d, 7)
        assert "stratum" not in open(os.path.join(d, "task_list.csv")).read()
        assert hashlib.sha256(open(os.path.join(d, "sealed_labels.json"), "rb").read()).hexdigest() == h
    print("self-check passed")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        self_check(); sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("frame"); ap.add_argument("--v-cap", type=int, default=1); ap.add_argument("--n-count", type=int, default=6)
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.frame)))
    print("seal hash:", write(draw(rows, a.v_cap, a.n_count, a.seed), a.out, a.seed))
