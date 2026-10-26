"""Draw the three development protocols (step 0 in README.md; proposal section 8, "Fixed development design").

Usage:
  python3 draw_protocols.py protocol_frame.csv --count 3 --seed <integer> --out drawn_protocols.csv
  python3 draw_protocols.py --self-check

protocol_frame.csv has one row per eligible protocol audit, with columns: protocol_id, n_eligible (its eligible N count).
The size measure is n_eligible, or 1 when it is 0. Inclusion probabilities are proportional to it, capped at 1 for very
large protocols, and sum to --count. Selection is randomized systematic sampling: random order, random start, then every
unit whose cumulative probability interval contains a selection point. This is the procedure of proposal section 5.2.
The output lists the drawn protocols with their inclusion probabilities and the seed. Record its SHA-256 in the timesheet.
Exposure to a drawn protocol's audit changes who does the blind steps, not which protocols are in the sample.
"""
import argparse, csv, hashlib, random, sys


def inclusion_probabilities(sizes, count):
    sizes = [max(s, 1) for s in sizes]
    certain = set()
    while True:
        rest = [i for i in range(len(sizes)) if i not in certain]
        total = sum(sizes[i] for i in rest)
        pi = [1.0 if i in certain else (count - len(certain)) * sizes[i] / total for i in range(len(sizes))]
        over = {i for i in rest if pi[i] > 1}
        if not over:
            return pi
        certain |= over


def draw(rows, count, seed):
    rng = random.Random(seed)
    pi = inclusion_probabilities([int(r["n_eligible"]) for r in rows], count)
    order = list(range(len(rows))); rng.shuffle(order)
    start, cum, picked, k = rng.random(), 0.0, [], 0
    for i in order:
        cum += pi[i]
        while k < count and start + k < cum:
            picked.append(i); k += 1
    assert len(set(picked)) == count, "a protocol was selected twice"
    return [dict(rows[i], inclusion_probability=pi[i]) for i in picked]


def self_check():
    rows = [{"protocol_id": f"P{i}", "n_eligible": str(n)} for i, n in enumerate([0, 10, 40, 300, 60, 25, 90, 5])]
    pi = inclusion_probabilities([int(r["n_eligible"]) for r in rows], 3)
    assert abs(sum(pi) - 3) < 1e-9 and max(pi) <= 1 + 1e-12 and pi[3] == 1.0
    hits = [0] * len(rows)
    for s in range(20000):
        for r in draw(rows, 3, s):
            hits[int(r["protocol_id"][1:])] += 1
    assert all(abs(h / 20000 - p) < 0.02 for h, p in zip(hits, pi)), (hits, pi)
    assert draw(rows, 3, 7) == draw(rows, 3, 7), "same seed must give the same sample"
    print("self-check passed")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        self_check(); sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("frame"); ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--seed", type=int, required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.frame)))
    drawn = draw(rows, a.count, a.seed)
    with open(a.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol_id", "n_eligible", "inclusion_probability", "seed"])
        for r in drawn:
            w.writerow([r["protocol_id"], r["n_eligible"], f"{r['inclusion_probability']:.6f}", a.seed])
    print("sha256:", hashlib.sha256(open(a.out, "rb").read()).hexdigest())
