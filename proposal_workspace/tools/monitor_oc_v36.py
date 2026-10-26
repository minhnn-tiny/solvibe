"""Version 36: how often the proposed unresolved-outcome rules fire (round-20 points R20.2 and R20.3).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with scipy python monitor_oc_v36.py
Rule: an author is outside the frozen operating region when its one-sided 95% exact (Clopper-Pearson) lower confidence limit
for the unresolved rate exceeds that author's limit. The region is the set passing under all four mechanisms in
power_results_v35.txt: vectors (u_A1, u_A2, u_H) no larger than (0.0075, 0.013, 0.0075), (0.013, 0.0075, 0.0075) or
(0.013, 0.013, 0.005). The vector of lower limits is "outside" when it is not inside that set.
Counts: each protocol contributes m built functions (one historical outcome each) and 2m outcomes per configuration.
Main study: 22 protocols, m = 5 or 6. Development: 3 protocols, m = 6 or 7.
Mechanisms: independent outcomes; protocol-shared (all of an author's outcomes in a protocol are unresolved together with
probability u). 200,000 simulated studies per row.
Two rules are compared. "binomial": the limit treats all of an author's outcomes as independent trials. "protocol": the limit
is the one-sided 95% exact lower limit for the share of protocols in which the author has at least one unresolved outcome,
divided by the largest number of that author's outcomes in one protocol. Under either mechanism the chance that a protocol
has an unresolved outcome is at most (outcomes per protocol) x u, so the protocol rule's limit stays below u in both.
"""
import numpy as np
from scipy import stats

MAXI = [(0.0075, 0.013, 0.0075), (0.013, 0.0075, 0.0075), (0.013, 0.013, 0.005)]


def lower(x, n):
    return np.where(x > 0, stats.beta.ppf(0.05, np.maximum(x, 1), n - x + 1), 0.0)


def fires(xs, ns):
    lo = np.stack([lower(x, n) for x, n in zip(xs, ns)], 1)             # (sims, 3): A1, A2, H
    inside = np.zeros(len(lo), bool)
    for mv in MAXI:
        inside |= (lo <= np.array(mv) + 1e-12).all(1)
    return ~inside


def run(rng, P, m, u, mech, rule, sims=200_000):
    per = [2 * m, 2 * m, m]
    if mech == "independent":
        xp = [rng.binomial(k, ua, (sims, P)) for k, ua in zip(per, u)]          # unresolved count per protocol
    else:
        xp = [rng.binomial(1, ua, (sims, P)) * k for k, ua in zip(per, u)]
    if rule == "binomial":
        return fires([x.sum(1) for x in xp], [k * P for k in per]).mean()
    lo = np.stack([lower((x > 0).sum(1), P) / k for x, k in zip(xp, per)], 1)
    inside = np.zeros(sims, bool)
    for mv in MAXI:
        inside |= (lo <= np.array(mv) + 1e-12).all(1)
    return (~inside).mean()


if __name__ == "__main__":
    rng = np.random.default_rng(3601)
    vecs = [(0.0, 0.0, 0.0), (0.005, 0.005, 0.005), (0.0075, 0.0075, 0.0075), (0.0075, 0.013, 0.0075), (0.013, 0.013, 0.005),
            (0.0, 0.0, 0.013), (0.0, 0.0, 0.02), (0.0, 0.0, 0.03), (0.0, 0.0, 0.065), (0.02, 0.02, 0.0075), (0.03, 0.03, 0.03)]
    for label, P, ms in (("main study, 22 protocols", 22, (5, 6)), ("development, 3 protocols", 3, (6, 7))):
        print(label)
        for rule in ("binomial", "protocol"):
            for mech in ("independent", "protocol"):
                for m in ms:
                    cells = "; ".join(f"{v}: {run(rng, P, m, v, mech, rule):.3f}" for v in vecs)
                    print(f"  rule {rule}, mechanism {mech}, {m} built functions per protocol: share of studies outside the region: {cells}")
    print("done")
