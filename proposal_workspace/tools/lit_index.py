"""Merge the paper blocks of every lit/r*_*.md file into one index, deduplicated by title.

Usage: python3 tools/lit_index.py [lit dir] > lit/master_index.tsv
Prints one row per distinct paper: best tier, status, venue, files it appears in, and its title.
A paper counts as VERIFIED if any file verified it.
"""
import glob, os, re, sys

lit = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "lit")


def norm(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


papers = {}
for path in sorted(glob.glob(os.path.join(lit, "r*_*.md"))):
    for block in re.split(r"\n(?=### )", open(path).read()):
        if not block.startswith("### "):
            continue
        head = block.splitlines()[0][4:].strip()
        pid, _, title = head.partition(" ")
        tier = re.search(r"^- Tier:\s*([ABC])", block, re.M)
        status = re.search(r"^- Status:\s*(\w+)", block, re.M)
        venue = re.search(r"Venue:\s*([^\n]*)", block)
        if not tier:
            continue
        key = norm(title or pid)
        p = papers.setdefault(key, {"title": title or pid, "tiers": set(), "status": set(), "venue": "", "files": set(), "ids": set()})
        p["tiers"].add(tier.group(1))
        p["status"].add(status.group(1) if status else "?")
        p["venue"] = p["venue"] or (venue.group(1)[:80] if venue else "")
        p["files"].add(os.path.basename(path).split("_")[1])
        p["ids"].add(pid)

print("tier\tstatus\tvenue\tfiles\tids\ttitle")
for p in sorted(papers.values(), key=lambda p: (min(p["tiers"]), p["title"].lower())):
    status = "VERIFIED" if "VERIFIED" in p["status"] else "UNVERIFIED"
    print("\t".join([min(p["tiers"]), status, p["venue"], ",".join(sorted(p["files"])), ",".join(sorted(p["ids"])), p["title"]]))

if __name__ == "__main__":
    # self-check on a tiny sample
    assert norm("Is Vibe Coding Safe?") == norm("is vibe-coding safe")
