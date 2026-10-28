from fetch_firm_reports import file_date, in_range


def test_file_date():
    assert file_date("2026-10-08-cyfrin-dowgo-v2.0.md") == "2026-10-08"
    assert file_date("Pare-security-review_2026-09-28.pdf") == "2026-09-28"
    assert file_date("2026.09.21 - Final - Maple Collaborative Audit Report 1789995803.pdf") == "2026-09-21"
    assert file_date("2026-10-offchain-labs-glamsterdam-gas-parameters-securityreview.pdf") == "2026-10"
    assert file_date("2025-1-everstake-ethereum-staking-protocol-securityreview.pdf") is None
    assert file_date("1inchTokenPlugins-security-review.md") is None


def test_in_range():
    assert in_range("2025-08", "2025-08-01", "2026-10-27") and in_range("2026-10", "2025-08-01", "2026-10-27")
    assert in_range("2025-08-01", "2025-08-01", "2026-10-27") and in_range("2026-10-27", "2025-08-01", "2026-10-27")
    assert not in_range("2025-07-31", "2025-08-01", "2026-10-27") and not in_range("2026-10-28", "2025-08-01", "2026-10-27")
    assert not in_range("2025-07", "2025-08-01", "2026-10-27") and not in_range(None, "2025-08-01", "2026-10-27")
