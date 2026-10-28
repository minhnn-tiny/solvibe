#!/usr/bin/env python3
"""Split the reports downloaded by fetch_firm_reports.py into one record per High/Medium Solidity finding.

Records use Solodit's field names (id, title, content, impact, firm_name, protocol_name, report_date, *_link), so
data_collection/extract_contracts.py runs on them unchanged. Findings already in the old Solodit download
(batches 1-4), or repeated across the new reports, are dropped and logged.

Usage: python3 -I scripts/split_firm_reports.py [--raw data_collection/downloaded_findings/batch_5_raw]
Writes data_collection/downloaded_findings/batch_5_firm_findings.json and batch_5_firm_findings/<id>.md (git-ignored),
plus data_collection/batch_5_reports.csv (one row per report) and batch_5_duplicates.csv (one row per dropped finding).
"""
import argparse, collections, csv, difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path

import lxml.etree
import lxml.html

ROOT = Path(__file__).resolve().parent.parent
DL = ROOT / "data_collection/downloaded_findings"
MONO = re.compile(r"mono|courier|consol|menlo|code|inconsolata|jetbrains|fira ?code|sfmono|sftt|sfit|cmtt|cmitt|typewriter",
                  re.I)


# ---------- HTML -> markdown (Code4rena report pages) ----------

def html_md(el):
    """Markdown for an lxml element: headings, paragraphs, lists, code, links. Anything else keeps its text."""
    tag = el.tag if isinstance(el.tag, str) else ""
    inner = lambda: (el.text or "") + "".join(html_md(c) + (c.tail or "") for c in el)
    if tag in ("svg", "style", "script", "img"):
        return ""
    if tag == "pre":
        lang = re.search(r"language-(\w+)", " ".join(c.get("class") or "" for c in el.iter()))
        return f"\n\n```{lang[1] if lang else ''}\n{el.text_content().rstrip()}\n```\n\n"
    if tag == "code":
        return f"`{el.text_content()}`"
    if tag == "a":
        text, href = inner().strip(), el.get("href") or ""
        if not href.startswith("http"):  # in-page anchors such as heading permalinks
            return text
        return href if text in ("", href) else f"[{text}]({href})"
    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return f"\n\n{'#' * int(tag[1])} {inner().strip()}\n\n"
    if tag in ("p", "div", "details", "table"):
        return f"\n\n{inner().strip()}\n\n"
    if tag in ("ul", "ol"):
        items = [html_md(li).strip().replace("\n", "\n  ") for li in el if li.tag == "li"]
        marks = [f"{i}." for i in range(1, len(items) + 1)] if tag == "ol" else ["-"] * len(items)
        return "\n\n" + "\n".join(f"{m} {t}" for m, t in zip(marks, items)) + "\n\n"
    if tag == "blockquote":
        return "\n\n" + "\n".join("> " + l for l in inner().strip().splitlines()) + "\n\n"
    if tag in ("strong", "b"):
        return f"**{inner().strip()}**"
    if tag in ("em", "i"):
        return f"_{inner().strip()}_"
    if tag == "br":
        return "\n"
    if tag == "tr":
        return "| " + " | ".join(html_md(c).strip() for c in el) + " |\n"
    if tag == "summary":
        return f"\n\n**{inner().strip()}**\n\n"
    return inner()


def tidy(md):
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+\n", "\n", md)).strip()


# ---------- PDF -> markdown (via poppler's pdftohtml -xml) ----------

def pdf_md(path):
    """Markdown-like text for a PDF: monospace lines become ``` blocks, larger fonts become headings,
    links keep their target, and lines repeated on most pages (headers, footers) are dropped."""
    xml = subprocess.run(["pdftohtml", "-xml", "-i", "-stdout", "-q", "-nodrm", str(path)],
                         capture_output=True, check=True).stdout
    root = lxml.etree.fromstring(xml, lxml.etree.XMLParser(recover=True, huge_tree=True))
    fonts = {f.get("id"): (float(f.get("size")), bool(MONO.search(f.get("family") or ""))) for f in root.iter("fontspec")}
    pages, sizes = [], collections.Counter()
    for page in root.iter("page"):
        height, frags = float(page.get("height")), []
        for t in page.iter("text"):
            size, mono = fonts.get(t.get("font"), (0, False))
            text = "".join(t.itertext())
            if not text.strip():
                continue
            for a in t.iter("a"):  # keep link targets: "label" -> "[label](href)"
                href, label = a.get("href") or "", "".join(a.itertext())
                if href.startswith("http") and label.strip() and label.strip() != href:
                    text = text.replace(label, f"[{label}]({href})", 1)
            top, h, left, w = (float(t.get(k)) for k in ("top", "height", "left", "width"))
            frags.append(dict(top=top, bottom=top + h, left=left, right=left + w, text=text, size=size, mono=mono,
                              cw=w / max(1, len(text))))
            sizes[size] += len(text)
        lines = []  # a fragment joins a line when their vertical extents overlap by half the smaller height
        for f in sorted(frags, key=lambda f: (f["top"], f["left"])):
            for l in reversed(lines[-3:]):
                overlap = min(l["bottom"], f["bottom"]) - max(l["top"], f["top"])
                if overlap >= 0.5 * min(l["bottom"] - l["top"], f["bottom"] - f["top"]):
                    l["frags"].append(f)
                    break
            else:
                lines.append(dict(top=f["top"], bottom=f["bottom"], frags=[f]))
        for l in lines:
            l["frags"].sort(key=lambda f: f["left"])
            for a, b in zip(l["frags"], l["frags"][1:]):  # a visible gap between fragments is a space
                if b["left"] - a["right"] > 0.15 * max(a["size"], 1) and not a["text"].endswith(" "):
                    a["text"] += " "
            l["top"] /= height
        pages.append(lines)
    body = sizes.most_common(1)[0][0] if sizes else 0
    # header/footer = same text (digits ignored) near the top or bottom of at least 40% of the pages
    edge = collections.Counter()
    for lines in pages:
        for l in {re.sub(r"\d+", "#", "".join(f["text"] for f in l["frags"]).strip()) for l in lines
                  if l["top"] < 0.08 or l["top"] > 0.92}:
            edge[l] += 1
    repeated = {k for k, n in edge.items() if len(pages) > 2 and n >= 0.4 * len(pages)}
    out, code = [], []

    def flush():
        if code:
            left0 = min(l for l, _, cw in code)
            out.append("```\n" + "\n".join(" " * round((l - left0) / max(cw, 1)) + t for l, t, cw in code) + "\n```")
            code.clear()

    for lines in pages:
        for l in lines:
            text = "".join(f["text"] for f in l["frags"]).strip()
            if (l["top"] < 0.08 or l["top"] > 0.92) and re.sub(r"\d+", "#", text) in repeated:
                continue
            mono_chars = sum(len(f["text"].strip()) for f in l["frags"] if f["mono"])
            heading_size = max(f["size"] for f in l["frags"]) >= body * 1.15  # code font inside a heading
            if mono_chars >= 0.8 * len(text.replace(" ", "").replace(",!", "")) and not heading_size:
                line = "".join(f["text"] for f in l["frags"]).rstrip()
                if code and line.lstrip().startswith(",!"):  # LaTeX listings wrapped this line
                    left, prev, cw = code.pop()
                    line = (prev[:-2] if prev.endswith(" c") else prev + " ") + line.lstrip()[2:].lstrip()
                    code.append((left, line, cw))
                else:
                    code.append((l["frags"][0]["left"], line, min(f["cw"] for f in l["frags"])))
                continue
            flush()
            size = max(f["size"] for f in l["frags"])
            text = "".join(f"`{f['text'].strip()}` " if f["mono"] and f["text"].strip() else f["text"]
                           for f in l["frags"]).strip()
            if size >= body * 1.15 and len(text) < 200:
                out.append("\n" + "#" * (2 if size >= body * 1.6 else 3) + " " + text + "\n")
            else:
                out.append(text)
    flush()
    md = unicodedata.normalize("NFKC", "\n".join(out))
    md = re.sub(r" c\n\s*,! ?", "", md)  # LaTeX listings: "Foo c" + ",! Bar" is one word broken across lines
    return tidy(re.sub(r"\n\s*,! ?", " ", md))  # ",!" marks a wrapped line


# ---------- report text -> findings: list of dict(severity, label, title, body, link) ----------

SEV = {"critical": "HIGH", "high": "HIGH", "medium": "MEDIUM"}  # Solodit files Critical under HIGH
LETTER = {"C": "critical", "H": "high", "M": "medium", "L": "low", "I": "informational", "G": "gas", "N": "informational",
          "Q": "low"}


def code4rena_findings(path):
    doc = lxml.html.parse(str(path)).getroot()
    head = doc.xpath('//div[@class="report-header"]')
    protocol = re.sub(r"\s*Findings\s*&\s*Analysis Report\s*$", "", head[0].findtext("h1") or "").strip() if head else ""
    published = (head[0].findtext("h4") or "").strip() if head else ""
    body = doc.xpath('//div[contains(@class,"report-contents")]')
    findings, section, cur = [], "", None
    for el in body[0] if body else []:
        if el.tag == "h1":
            section, cur = el.text_content().strip().lower(), None
        elif el.tag == "h2" and ("high risk" in section or "medium risk" in section):
            for c in el.iter("code"):  # keep inline code marks in the title, as Solodit does
                c.text = f"`{c.text_content()}`"
                c[:] = []
            title = el.text_content().strip()
            m = re.match(r"\[?([HM])-(\d+)\]?", title)
            link = next((a.get("href") for a in el.iter("a") if (a.get("href") or "").startswith("http")), "")
            cur = dict(severity=LETTER[m[1]] if m else section.split()[0], label=f"{m[1]}-{m[2]}" if m else "",
                       title=title, body="", link=link)
            findings.append(cur)
        elif cur is not None and not (el.tag == "p" and el.text_content().strip().startswith("Submitted by")):
            cur["body"] += html_md(el)
    for f in findings:
        f["body"] = tidy(f["body"])
    return findings, protocol, published


def heading_findings(md, section_re, finding_re, start_re=None):
    """Findings in markdown where a section heading names the severity and each finding starts at its own line.
    section_re: group 'sev'. finding_re: group 'title', optional 'label'. Text before start_re is skipped."""
    if start_re:
        starts = [m.end() for m in re.finditer(start_re, md, re.M)]
        md = md[starts[-1]:] if starts else md
    findings, severity = [], None
    for line in md.splitlines(keepends=True):
        s = section_re and re.match(section_re, line.strip(), re.I)
        if s:
            severity = s["sev"].lower()
            findings.append(None)  # a section heading ends the previous finding
            continue
        m = re.match(finding_re, line.rstrip("\n"))
        label = (m.groupdict().get("label") or "") if m else ""
        if m and (severity or label):
            sev = LETTER.get(label[:1].upper(), severity) if label else severity
            findings.append(dict(severity=sev, label=label, title=m["title"].strip(), body="", link=""))
        elif findings and findings[-1] is not None:
            findings[-1]["body"] += line
    out = [f for f in findings if f]
    for f in out:
        f["body"] = tidy(f["body"])
    return out


def wrapped_title(f, first_label=r"(Description|Summary|Severity|Impact|Context|Vulnerability Detail|Location)\b|"
                                 r"(Critical|High|Medium|Low)\s+(Fixed|Resolved|Acknowledged|Pending|Open)\b|"
                                 r"(Acknowledged|Resolved|Fixed)$"):
    """PDF titles can wrap; move body lines before the first section label back into the title."""
    lines = f["body"].splitlines()
    for i, l in enumerate(lines[:4]):
        if re.match(first_label, l.strip(" *#_"), re.I):
            if i:
                f["title"] = " ".join([f["title"]] + [x.strip() for x in lines[:i]])
                f["body"] = "\n".join(lines[i:])
            break
    return f


def cyfrin_findings(md, fmt):
    sec = r"^(?:#+\s*)?(?:\d+\.\d+\s+)?(?P<sev>Critical|High|Medium|Low|Informational|Gas Optimizations?)(?:\s+Risk)?$"
    if fmt == "md":
        return heading_findings(md, sec, r"^###\s+(?P<title>.+)$", r"^# Findings\s*$")
    out = heading_findings(md, sec, r"^(?:#+\s*)?\d+\.\d+\.\d+\s+(?P<title>.+)$", r"^(?:#+\s*)?\d+\s+Findings\s*$")
    return [wrapped_title(f) for f in out]


def pashov_findings(md, fmt):
    """Team reports: '# [H-01] title' after '# Findings'; agentic reports: '#### [M-01] title'. The label gives the severity."""
    out = heading_findings(md, None, r"^(?:#{1,4}\s*)?\[(?P<label>[CHMLIG]-\d+)\](?!\()\s*(?P<title>.+)$",  # not '[M-7](url)'
                           r"^#{1,3}\s*(?:\d+\s+)?Findings\s*$")
    return [wrapped_title(f) for f in out] if fmt == "pdf" else out


def tob_findings(md, fmt):
    """'N. Title' (may wrap) then 'Severity: X Difficulty: Y' within 3 lines, under the last 'Detailed Findings'.
    Section labels become headings, as in Solodit's copies, so extract_contracts.py can find them."""
    starts = [m.end() for m in re.finditer(r"^(?:#+\s*)?Detailed Findings\s*$", md, re.M)]
    lines = md[starts[-1]:].splitlines() if starts else []
    out, i = [], 0
    while i < len(lines):
        if re.match(r"^(?:#+\s*)?[A-Z]\.\s+[A-Z]", lines[i]):  # appendix A., B., ... ends the findings
            break
        m = re.match(r"^(?:#+\s*)?(\d{1,3})\.\s+(.+)$", lines[i])
        sev_at = next((j for j in range(i + 1, min(i + 4, len(lines))) if lines[j].startswith("Severity:")), None)
        if m and sev_at:
            sev = re.match(r"Severity:\s*(\w+)", lines[sev_at])[1].lower()
            out.append(dict(severity=sev, label="", title=" ".join([m[2]] + [l.strip() for l in lines[i + 1:sev_at]]),
                            body="", link=""))
            i = sev_at
            continue
        if out:
            out[-1]["body"] += lines[i] + "\n"
        i += 1
    for f in out:
        fid = re.search(r"Finding ID:\s*(TOB-[\w-]+)", f["body"])
        f["label"] = fid[1] if fid else ""
        f["body"] = tidy(re.sub(r"^(Description|Exploit Scenario|Recommendations?)\s*$", r"## \1", f["body"], flags=re.M))
    return out


def sherlock_findings(md, fmt):
    """'Issue H-1: title [RESOLVED]' in a large font, so long titles wrap over several heading lines."""
    lines, out, i = md.splitlines(), [], 0
    while i < len(lines):
        m = re.match(r"^(?:#+\s*)?Issue\s+(?P<label>[CHML]-\d+):\s*(?P<title>.+)$", lines[i])
        if m:
            title, j = m["title"].strip(), i + 1
            while j < len(lines) and (not lines[j].strip() or re.match(r"^#+\s", lines[j]) and not re.match(
                    r"^#+\s*(Issue\s|Summary|Source|Vulnerability Detail|Root Cause)", lines[j])):
                part = lines[j].lstrip("# ").strip()
                title += part if title.endswith("-") or not part else " " + part
                j += 1
            out.append(dict(severity=LETTER[m["label"][0]], label=m["label"], body="", link="",
                            title=re.sub(r"\s*\[[A-Z][A-Z\- ]*\]\s*$", "", title)))
            i = j
            continue
        if out:
            out[-1]["body"] += lines[i] + "\n"
        i += 1
    for f in out:
        f["body"] = tidy(f["body"])
    return out


def longest_per_label(findings):
    """A label seen twice in one report (summary table first, then the finding) keeps the copy with the most text."""
    best = {}
    for n, f in enumerate(findings):
        key = f["label"] or n
        if key not in best or len(f["body"]) > len(best[key]["body"]):
            best[key] = f
    return list(best.values())


def solodit_content_findings(md, fmt):
    """Solodit's own report repo: '# Findings', '## High Risk', '### [H-01] title' (the label is optional)."""
    sec = r"^#{1,3}\s*(?P<sev>Critical|High|Medium|Low|Informational|Gas Optimizations?)(?:\s+Risk)?$"
    return heading_findings(md, sec, r"^###\s+(?:\[(?P<label>[CHMLIG]-\d+)\]\s*)?(?P<title>.+)$", r"^# Findings\s*$")


# ---------- Solidity check ----------

SOL = re.compile(r"\.sol\b|```solidity|pragma solidity|\buint256\b|msg\.sender|\bmapping\s*\(|\brequire\(|\bemit\s|"
                 r"\b(?:external|public)\s+(?:view|pure|payable|returns)\b|\bonlyOwner\b")
OTHER = re.compile(r"\.(?:rs|move|cairo|go|vy|tsx?|fc|func|tact|nr|circom|sw)\b|```(?:rust|move|cairo|go|vyper|typescript|ts|"
                   r"javascript|js|python|py)\b|\bpub\s+fn\b|\bfn\s+\w+\s*\(|\blet\s+mut\b|#\[account|\bPubkey\b|"
                   r"ctx\.accounts|\bfelt252\b|\bpublic\s+(?:entry\s+)?fun\b|\bfunc\s+\(?\w")


def solidity_score(text):
    return len(SOL.findall(text)) - len(OTHER.findall(text))


# ---------- records, duplicates, output ----------

GENERIC = {"cyfrin", "security", "review", "securityreview", "final", "collaborative", "audit", "report", "fv", "and", "agentic",
           "the", "of", "protocol", "contracts", "smart", "contract", "update", "updates", "diff", "fix", "review2",
           "public", "best", "efforts", "contest"}


def protocol_from_stem(stem):
    stem = re.sub(r"20\d\d[-_.]\d{1,2}(?:[-_.]\d{1,2})?|\b\d{6,}\b|-v\d+(?:\.\d+)*|\bv\d+\.\d+", " ", stem)
    words = [w for w in re.split(r"[-_ .]+", stem) if w and w.lower() not in GENERIC]
    return " ".join(w if any(c.isupper() for c in w) else w.capitalize() for w in words)


def tokens(protocol):
    return {w for w in re.findall(r"[a-z0-9]+", protocol.lower()) if w not in GENERIC and not re.fullmatch(r"v?\d+", w)}


def norm_title(title):
    t = unicodedata.normalize("NFKC", title).lower()
    t = re.sub(r"^\s*(?:issue\s+)?(?:\[?[a-z]{1,4}-[a-z]*-?\d+\]?|\d+(?:\.\d+)*\.?)\s*[:.\-]?\s*", "", t)
    return " ".join(re.findall(r"[a-z0-9]+", t))


def report_key(link):
    """File stem or Code4rena contest slug a finding came from, e.g. '2026-03-13-cyfrin-myriad-clob-v2.0'."""
    m = re.search(r"code4rena\.com/(?:reports|audits)/([^/?#]+)", link or "")
    return m[1] if m else Path(re.sub(r"[?#].*", "", link or "")).stem.lower()


def duplicate_score(new, old):
    """2 = same title, 1 = nearly the same title (PDF wrapping, punctuation), 0 = different finding.
    Both must come from one firm and the same report, or from reports on the same protocol: a shared client
    name alone is not enough, because generic titles repeat across different audits of one client."""
    if new["firm_name"] != old["firm_name"]:
        return 0
    same_report = bool(new["report_key"]) and new["report_key"] in old["report_keys"]
    union, overlap = new["tokens"] | old["tokens"], new["tokens"] & old["tokens"]
    contained = bool(overlap) and overlap in (new["tokens"], old["tokens"])  # 'Mellow' vs 'Mellow Flexible Vaults'
    if not (same_report or contained or (union and len(overlap) >= 0.5 * len(union))):
        return 0
    if new["title_norm"] == old["title_norm"]:
        return 2
    return int(difflib.SequenceMatcher(None, new["title_norm"], old["title_norm"]).ratio() >= 0.95)


def best_match(new, pool):
    score, match = max(((duplicate_score(new, o), o) for o in pool), key=lambda t: t[0], default=(0, None))
    return match if score else None


def old_index():
    """Old Solodit findings (batches 1-4) by firm, with the fields is_duplicate needs."""
    by_firm = collections.defaultdict(list)
    for batch in sorted(DL.glob("batch_*_solodit_findings.json")):
        for f in json.loads(batch.read_text()):
            links = [f.get(k) or "" for k in ("source_link", "github_link", "contest_link", "pdf_link")]
            by_firm[f["firm_name"]].append(dict(id=str(f["id"]), firm_name=f["firm_name"], title_norm=norm_title(f["title"]),
                                                tokens=tokens(f.get("protocol_name") or ""),
                                                report_keys={report_key(l) for l in links if l}))
    return by_firm


SHORT = {"code4rena": "c4", "cyfrin": "cyfrin", "pashov": "pashov", "trailofbits": "tob", "sherlock": "sherlock"}


def make_record(r, f, protocol, published, n):
    label = f["label"] or f"{f['severity'][0].upper()}-{n:02d}"
    source = SHORT.get(r["source"]) or re.sub(r"[^a-z0-9]+", "", r["firm"].lower())
    rid = re.sub(r"[^A-Za-z0-9.]+", "-", f"{source}-{r['date']}-{protocol.lower()}-{label}").strip("-")
    url = r["url"]
    return dict(id=rid, kind={"md": "MARKDOWN", "pdf": "PDF", "html": "HTML"}[r["format"]],
                impact=SEV[f["severity"]], title=f["title"], content=f["body"], summary="", report_date=r["date"],
                firm_name=r["firm"], protocol_name=protocol, source_link=url,
                github_link=f["link"] or (url if "github.com" in url else ""), github_link_valid=True,
                contest_link=url if r["source"] == "code4rena" else "", pdf_link=url if r["format"] == "pdf" else "",
                source=r["source"], report_path=r["local_path"], finding_label=label, severity_raw=f["severity"],
                report_published=published or r["date"])


def report_findings(r):
    """(findings, protocol, publication date, solidity score of the whole report) for one downloaded report."""
    path, fmt, src = ROOT / r["local_path"], r["format"], r["source"]
    if src == "code4rena":
        fs, protocol, published = code4rena_findings(path)
        return longest_per_label(fs), protocol, published, solidity_score(path.read_text(errors="replace"))
    text = path.read_text(errors="replace") if fmt == "md" else pdf_md(path)
    return longest_per_label(PARSERS[src](text, fmt)), protocol_from_stem(Path(r["path"]).stem), "", solidity_score(text)


PARSERS = {"cyfrin": cyfrin_findings, "pashov": pashov_findings, "trailofbits": tob_findings,
           "sherlock": sherlock_findings, "solodit_content": solodit_content_findings}


def collect(reports, old):
    """(one row per report, all Solidity High/Medium findings, the findings kept, the duplicates dropped)."""
    rows, kept, dups, candidates = [], [], [], []
    for r in reports:
        fs, protocol, published, report_score = report_findings(r)
        hm = [f for f in fs if f["severity"] in SEV]
        # a finding with no language signal of its own follows its report, if the report is clearly Solidity
        sol = [f for f in hm if (s := solidity_score(f["title"] + "\n" + f["body"])) > 0 or (s == 0 and report_score >= 10)]
        rows.append(dict(source=r["source"], firm=r["firm"], date=r["date"], report=r["path"], format=r["format"],
                         protocol=protocol, published=published, findings_all=len(fs), high_medium=len(hm),
                         solidity_high_medium=len(sol), report_solidity_score=report_score, url=r["url"]))
        per_severity = collections.Counter()
        for f in sol:
            per_severity[f["severity"]] += 1
            rec = make_record(r, f, protocol, published, per_severity[f["severity"]])
            rec.update(title_norm=norm_title(rec["title"]), tokens=tokens(protocol), report_key=report_key(r["url"]))
            candidates.append(rec)
    # earliest report first, markdown before PDF, so the copy kept is the first public one
    candidates.sort(key=lambda c: (c["report_date"], c["kind"] != "MARKDOWN", c["id"]))
    seen_ids = collections.Counter()
    for c in candidates:
        match = best_match(c, old.get(c["firm_name"], []))
        twin = None if match else best_match(c, [dict(k, report_keys={k["report_key"]}) for k in kept
                                                 if k["firm_name"] == c["firm_name"]])
        if match or twin:
            dups.append(dict(id=c["id"], firm=c["firm_name"], date=c["report_date"], title=c["title"],
                             duplicate_of=match["id"] if match else twin["id"],
                             where="old Solodit download" if match else "new reports", report=c["report_path"]))
            continue
        seen_ids[c["id"]] += 1
        if seen_ids[c["id"]] > 1:
            c["id"] += f"-{seen_ids[c['id']]}"
        kept.append(c)
    for c in kept:
        for k in ("title_norm", "tokens", "report_key"):
            c.pop(k)
    return rows, candidates, kept, dups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(DL / "batch_5_raw"))
    ap.add_argument("--name", default="batch_5_firm_findings")
    a = ap.parse_args()
    reports = json.loads((Path(a.raw) / "reports.json").read_text())
    rows, candidates, kept, dups = collect(reports, old_index())
    out_json, out_md = DL / f"{a.name}.json", DL / a.name
    out_md.mkdir(exist_ok=True)
    for old_md in out_md.glob("*.md"):
        old_md.unlink()
    out_json.write_text(json.dumps(kept, indent=1, ensure_ascii=False))
    for f in kept:  # same layout as download.py writes for Solodit findings
        (out_md / f"{f['id']}.md").write_text(
            f"# {f['title']}\n\n## Summary\n\n*No summary available*\n\n## GitHub Source Code\n\n"
            f"- **Link**: {f['github_link'] or 'N/A'}\n- **Valid**: {'✓ Yes' if f['github_link'] else '✗ No/Unknown'}\n\n"
            f"## Content\n\n{f['content']}", encoding="utf-8")
    for name, table in (("batch_5_reports.csv", rows), ("batch_5_duplicates.csv", dups)):
        with open(DL.parent / name, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(table[0]) if table else ["id"])
            w.writeheader()
            w.writerows(table)
    print(json.dumps(dict(reports=len(reports), high_medium=sum(r["high_medium"] for r in rows),
                          solidity_high_medium=len(candidates), duplicates=len(dups), kept=len(kept),
                          by_firm=collections.Counter(f["firm_name"] for f in kept), out=str(out_json)), indent=1))


if __name__ == "__main__":
    main()
