from filter_tier1_after_cutoff import failed_checks, finding_date, in_range, linked_month


def test_linked_month():
    assert linked_month({"github_link": "https://github.com/code-423n4/2025-10-hybra-finance"})[0] == 202510
    assert linked_month({"pdf_link": "x/Aragon-Spearbit-Security-Review-November-2025.pdf"})[0] == 202511
    assert linked_month({"pdf_link": "https://cdn.cantina.xyz/reports/cantina_tao_march2025.pdf"})[0] == 202503
    assert linked_month({"source_link": "reviews/2023-8-offchain-challenge.pdf"})[0] == 202308
    assert linked_month({"contest_link": "a/2025-02-recall", "pdf_link": "b/review_2025-11-21.md"}) == (202511, "b/review_2025-11-21.md")
    assert linked_month({"source_link": "https://blog.openzeppelin.com/usdt0-polygon-integration-audit"}) == (None, "")


def test_failed_checks():
    ok = dict(is_complete=True, has_pragma=True, has_contract=True, has_function=True, balanced_braces=True,
              problem_code={"has_problem_code": True}, validation={"content_code_consistency": {"consistent": True}})
    assert failed_checks(ok) == []
    assert failed_checks({**ok, "has_pragma": False, "validation": {}}) == ["has_pragma", "consistent"]


def test_finding_date():
    assert finding_date({"id": "x", "report_date": "2026-03-13"}, {}) == ("2026-03-13", "report file name")
    assert finding_date({"id": "y", "report_date": "2025-11", "source": "code4rena"}, {})[1] == "contest month in report URL"
    assert finding_date({"id": 1, "report_date": {}, "source_link": "a/2025-10-hybra"}, {}) == ("2025-10", "month in link")
    assert finding_date({"id": 2, "report_date": {}, "source_link": "b/no-date"}, {"2": "2025-11-03"})[0] == "2025-11-03"
    assert finding_date({"id": 3, "report_date": {}}, {}) == (None, "")


def test_in_range():
    assert in_range("2025-08", "2025-08-01", "2026-10-27") and in_range("2026-10-27", "2025-08-01", "2026-10-27")
    assert not in_range("2025-07-31", "2025-08-01", "2026-10-27") and not in_range("2026-11", "2025-08-01", "2026-10-27")
