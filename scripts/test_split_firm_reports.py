from split_firm_reports import duplicate_score, heading_findings, norm_title, protocol_from_stem, solidity_score, tokens


def test_norm_title():
    assert norm_title("[M-03] `fulfillRedeem` may corrupt share price") == "fulfillredeem may corrupt share price"
    assert norm_title("M-6: Interest accrual can get stuck") == norm_title("Issue M-6: Interest accrual can get stuck")
    assert norm_title("7.1.1 Voting power returns 0") == "voting power returns 0"
    assert norm_title("Deﬁcit reporting") == "deficit reporting"  # PDF ligature


def test_protocol_from_stem():
    assert protocol_from_stem("2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1") == "Securitize Dstoken Rebasing"
    assert protocol_from_stem("Ostium-security-review_2025-09-14") == "Ostium"
    assert protocol_from_stem("2026.09.21 - Final - Maple Collaborative Audit Report 1789995803") == "Maple"
    assert tokens("Ostium_2025-09-14") == {"ostium"} and tokens("Aave V4") == {"aave"}


def test_duplicate_score():
    a = dict(firm_name="Cyfrin", title_norm="x is wrong", report_key="r1", tokens={"linea", "yield", "manager"})
    same = dict(firm_name="Cyfrin", title_norm="x is wrong", report_keys={"r2"}, tokens={"linea", "yield", "manager"})
    assert duplicate_score(a, same) == 2
    assert duplicate_score(a, dict(same, firm_name="Pashov Audit Group")) == 0
    assert duplicate_score(a, dict(same, tokens={"securitize", "registry"})) == 0  # another audit, same title
    assert duplicate_score(a, dict(same, title_norm="y is wrong too")) == 0
    assert duplicate_score(a, dict(same, tokens=set(), report_keys={"r1"}, title_norm="x is wrongg")) == 1
    mellow = dict(a, firm_name="Sherlock", tokens=tokens(protocol_from_stem(
        "2025.09.08 - Final - Mellow Protocol Public Best Efforts Audit Contest Report 1757334246")))
    assert duplicate_score(mellow, dict(same, firm_name="Sherlock", tokens=tokens("Mellow Flexible Vaults"))) == 2


def test_solidity_score():
    assert solidity_score("`Vault.sol` uses msg.sender in require(") > 0
    assert solidity_score("```rust\npub fn withdraw(ctx: Context<W>)") < 0
    assert solidity_score("The admin can pause the bridge") == 0


def test_heading_findings():
    md = "intro\n# Findings\n## High Risk\n### A breaks\nbody a\n## Low Risk\n### B\nbody b\n"
    fs = heading_findings(md, r"^## (?P<sev>High|Low) Risk$", r"^### (?P<title>.+)$", r"^# Findings\s*$")
    assert [(f["severity"], f["title"], f["body"]) for f in fs] == [("high", "A breaks", "body a"), ("low", "B", "body b")]
