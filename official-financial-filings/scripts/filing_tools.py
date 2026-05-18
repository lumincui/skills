#!/usr/bin/env python3
"""Utilities for retrieving official financial filings and extracting source text/tables."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Mozilla/5.0 official-financial-filings-skill/1.1"
HKEX_BASE = "https://www1.hkexnews.hk"
CNINFO_QUERY_URL = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_STATIC_BASE = "http://static.cninfo.com.cn/"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clean_cik(cik: str) -> str:
    digits = re.sub(r"\D", "", cik)
    if not digits:
        raise SystemExit("CIK must contain digits")
    return digits.zfill(10)


def normalize_hk_code(code: str) -> str:
    digits = re.sub(r"\D", "", code)
    if not digits:
        raise SystemExit("HK stock code must contain digits")
    return digits.zfill(5)


def normalize_a_code(code: str) -> str:
    digits = re.sub(r"\D", "", code)
    if len(digits) != 6:
        raise SystemExit("A-share stock code must be 6 digits, e.g. 000338")
    return digits


def fetch(url: str, *, accept: str = "*/*", headers: dict[str, str] | None = None) -> bytes:
    req_headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    with urlopen(req, timeout=60) as response:
        return response.read()


def post_form(url: str, data: dict[str, str], *, headers: dict[str, str] | None = None) -> bytes:
    body = urlencode(data).encode("utf-8")
    req_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://www.cninfo.com.cn",
        "Referer": "http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search",
        "X-Requested-With": "XMLHttpRequest",
    }
    if headers:
        req_headers.update(headers)
    req = Request(url, data=body, headers=req_headers, method="POST")
    with urlopen(req, timeout=60) as response:
        return response.read()


def write_source_log(out_dir: Path, row: dict[str, str]) -> None:
    log_path = out_dir / "source_log.csv"
    fieldnames = [
        "company_name",
        "ticker_or_code",
        "listing_venue",
        "source_system",
        "document_type",
        "fiscal_period",
        "filing_or_announcement_date",
        "source_url",
        "source_identifier",
        "local_path",
        "retrieved_at",
        "notes",
    ]
    exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fieldnames})


def safe_filename(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\s]+", "_", value.strip())
    return value.strip("_")[:180] or "filing"


def sec_submissions(args: argparse.Namespace) -> None:
    cik = clean_cik(args.cik)
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = fetch(url, accept="application/json")
    out_path = out_dir / f"sec_submissions_CIK{cik}.json"
    out_path.write_bytes(data)
    write_source_log(out_dir, {"ticker_or_code": cik, "listing_venue": "US", "source_system": "SEC EDGAR submissions API", "document_type": "submissions index", "source_url": url, "source_identifier": f"CIK{cik}", "local_path": str(out_path), "retrieved_at": now_iso()})
    print(out_path)


def sec_companyfacts(args: argparse.Namespace) -> None:
    cik = clean_cik(args.cik)
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    data = fetch(url, accept="application/json")
    out_path = out_dir / f"sec_companyfacts_CIK{cik}.json"
    out_path.write_bytes(data)
    write_source_log(out_dir, {"ticker_or_code": cik, "listing_venue": "US", "source_system": "SEC EDGAR companyfacts API", "document_type": "XBRL company facts", "source_url": url, "source_identifier": f"CIK{cik}", "local_path": str(out_path), "retrieved_at": now_iso()})
    print(out_path)


def download(args: argparse.Namespace) -> None:
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    parsed = urlparse(args.url)
    name = args.filename or Path(parsed.path).name or "downloaded_filing"
    out_path = out_dir / name
    out_path.write_bytes(fetch(args.url))
    write_source_log(out_dir, {"source_system": args.source_system or parsed.netloc, "document_type": args.document_type or "official filing/document", "source_url": args.url, "source_identifier": args.source_identifier or "", "local_path": str(out_path), "retrieved_at": now_iso(), "notes": args.notes or ""})
    print(out_path)


def hkex_stock_id(code: str) -> tuple[str, str, str]:
    hk_code = normalize_hk_code(code)
    data = json.loads(fetch(f"{HKEX_BASE}/ncms/script/eds/activestock_sehk_e.json").decode("utf-8-sig"))
    for item in data:
        if item.get("c") == hk_code:
            return str(item["i"]), item["c"], item.get("n", "")
    raise SystemExit(f"HKEX active stock not found for code {hk_code}")


def hkex_query(code: str, date_from: str, date_to: str, doc_type: str, limit: int) -> list[dict[str, str]]:
    stock_id, hk_code, name = hkex_stock_id(code)
    t2code = {"annual": "4000", "interim": "4001", "quarterly": "4002", "esg": "4003", "all": ""}.get(doc_type)
    if t2code is None:
        raise SystemExit("HKEX --doc-type must be annual, interim, quarterly, esg, or all")
    params = {
        "sortDir": "0",
        "sortByOptions": "DateTime",
        "category": "0",
        "market": "SEHK",
        "stockId": stock_id,
        "documentType": "",
        "fromDate": date_from,
        "toDate": date_to,
        "title": "",
        "searchType": "1",
        "t1code": "40000",
        "t2Gcode": "",
        "t2code": t2code,
        "rowRange": str(limit),
        "lang": "en",
    }
    url = f"{HKEX_BASE}/search/titleSearchServlet.do?{urlencode(params)}"
    raw = fetch(url, accept="application/json", headers={"Referer": f"{HKEX_BASE}/search/titlesearch.xhtml?lang=en", "X-Requested-With": "XMLHttpRequest"}).decode("utf-8")
    response = json.loads(raw)
    items = json.loads(response.get("result", "[]"))
    filtered = []
    for item in items:
        item["RESOLVED_STOCK_ID"] = stock_id
        item["RESOLVED_STOCK_CODE"] = hk_code
        item["RESOLVED_STOCK_NAME"] = name
        item["SOURCE_URL"] = f"{HKEX_BASE}{item['FILE_LINK']}"
        item["TITLE"] = html.unescape(item.get("TITLE", ""))
        item["LONG_TEXT"] = html.unescape(item.get("LONG_TEXT", ""))
        title = item.get("TITLE", "").lower()
        long_text = item.get("LONG_TEXT", "").lower()
        if doc_type == "annual" and ("annual report" not in title or "environmental" in title or "esg" in title):
            continue
        if doc_type == "interim" and "interim" not in title.lower():
            continue
        if doc_type == "quarterly" and "quarter" not in title.lower():
            continue
        if doc_type == "esg" and "environmental" not in long_text and "esg" not in title:
            continue
        filtered.append(item)
    return filtered


def hkex_search(args: argparse.Namespace) -> None:
    items = hkex_query(args.code, args.date_from, args.date_to, args.doc_type, args.limit)
    print(json.dumps(items, ensure_ascii=False, indent=2))


def hkex_download_latest(args: argparse.Namespace) -> None:
    items = hkex_query(args.code, args.date_from, args.date_to, args.doc_type, args.limit)
    if not items:
        raise SystemExit("No HKEX filing found")
    item = items[0]
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    title = safe_filename(item.get("TITLE", "HKEX_filing"))
    code = item.get("STOCK_CODE", normalize_hk_code(args.code))
    filename = f"HKEX_{code}_{title}_{item.get('NEWS_ID','')}.pdf"
    out_path = out_dir / filename
    out_path.write_bytes(fetch(item["SOURCE_URL"]))
    write_source_log(out_dir, {"company_name": item.get("STOCK_NAME", ""), "ticker_or_code": code, "listing_venue": "Hong Kong", "source_system": "HKEXnews", "document_type": item.get("TITLE", args.doc_type), "filing_or_announcement_date": item.get("DATE_TIME", ""), "source_url": item["SOURCE_URL"], "source_identifier": item.get("NEWS_ID", ""), "local_path": str(out_path), "retrieved_at": now_iso(), "notes": item.get("LONG_TEXT", "")})
    print(out_path)


def cninfo_column(code: str) -> str:
    if code.startswith(("60", "68", "900")):
        return "sse"
    if code.startswith(("00", "30", "20")):
        return "szse"
    if code.startswith(("43", "83", "87", "92")):
        return "bj"
    return "szse"


def cninfo_stock_param(code: str) -> tuple[str, str, str]:
    a_code = normalize_a_code(code)
    metadata_urls = [
        "http://www.cninfo.com.cn/new/data/szse_stock.json",
        "http://www.cninfo.com.cn/new/data/bj_stock.json",
    ]
    for url in metadata_urls:
        data = json.loads(fetch(url, accept="application/json", headers={"Referer": "http://www.cninfo.com.cn/"}).decode("utf-8-sig"))
        for item in data.get("stockList", []):
            if item.get("code") == a_code:
                return f"{a_code},{item['orgId']}", item.get("zwjc", ""), item.get("orgId", "")
    raise SystemExit(f"CNINFO stock metadata not found for code {a_code}")


def cninfo_category(doc_type: str) -> str:
    mapping = {
        "annual": "category_ndbg_szsh",
        "interim": "category_bndbg_szsh",
        "quarterly": "category_yjdbg_szsh",
        "all": "",
    }
    if doc_type not in mapping:
        raise SystemExit("CNINFO --doc-type must be annual, interim, quarterly, or all")
    return mapping[doc_type]


def cninfo_query(code: str, date_from: str, date_to: str, doc_type: str, limit: int) -> list[dict[str, str]]:
    a_code = normalize_a_code(code)
    stock_param, stock_name, org_id = cninfo_stock_param(a_code)
    data = {
        "pageNum": "1",
        "pageSize": str(limit),
        "column": cninfo_column(a_code),
        "tabName": "fulltext",
        "plate": "",
        "stock": stock_param,
        "searchkey": "",
        "secid": "",
        "category": cninfo_category(doc_type),
        "trade": "",
        "seDate": f"{date_from}~{date_to}",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }
    raw = post_form(CNINFO_QUERY_URL, data).decode("utf-8")
    response = json.loads(raw)
    announcements = response.get("announcements") or []
    filtered = []
    for item in announcements:
        item["SOURCE_URL"] = CNINFO_STATIC_BASE + item["adjunctUrl"]
        item["announcementTitle"] = re.sub(r"<[^>]+>", "", item.get("announcementTitle", ""))
        item["RESOLVED_ORG_ID"] = org_id
        item["RESOLVED_STOCK_NAME"] = stock_name
        ts = item.get("announcementTime")
        if isinstance(ts, int):
            item["announcementDate"] = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
        title = item.get("announcementTitle", "")
        if doc_type != "all" and any(word in title for word in ["摘要", "取消", "英文", "已取消"]):
            continue
        filtered.append(item)
    return filtered


def cninfo_search(args: argparse.Namespace) -> None:
    items = cninfo_query(args.code, args.date_from, args.date_to, args.doc_type, args.limit)
    print(json.dumps(items, ensure_ascii=False, indent=2))


def cninfo_download_latest(args: argparse.Namespace) -> None:
    items = cninfo_query(args.code, args.date_from, args.date_to, args.doc_type, args.limit)
    if not items:
        raise SystemExit("No CNINFO filing found")
    item = items[0]
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    code = item.get("secCode", normalize_a_code(args.code))
    title = safe_filename(item.get("announcementTitle", "CNINFO_filing"))
    suffix = Path(urlparse(item["SOURCE_URL"]).path).suffix or ".pdf"
    filename = f"CNINFO_{code}_{title}_{item.get('announcementId','')}{suffix}"
    out_path = out_dir / filename
    out_path.write_bytes(fetch(item["SOURCE_URL"], headers={"Referer": "http://www.cninfo.com.cn/"}))
    write_source_log(out_dir, {"company_name": item.get("secName", ""), "ticker_or_code": code, "listing_venue": cninfo_column(code), "source_system": "CNINFO", "document_type": item.get("announcementTitle", args.doc_type), "filing_or_announcement_date": item.get("announcementDate", ""), "source_url": item["SOURCE_URL"], "source_identifier": str(item.get("announcementId", "")), "local_path": str(out_path), "retrieved_at": now_iso(), "notes": item.get("adjunctUrl", "")})
    print(out_path)


def extract_pdf(args: argparse.Namespace) -> None:
    try:
        import pdfplumber
    except ImportError as exc:
        raise SystemExit("Install pdfplumber first: python -m pip install pdfplumber") from exc
    pdf_path = Path(args.pdf)
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    text_path = out_dir / f"{pdf_path.stem}_text.txt"
    tables_dir = out_dir / f"{pdf_path.stem}_tables"
    ensure_dir(tables_dir)
    with pdfplumber.open(str(pdf_path)) as pdf, text_path.open("w", encoding="utf-8") as text_file:
        for page_num, page in enumerate(pdf.pages, start=1):
            text_file.write(f"\n\n--- Page {page_num} ---\n")
            text_file.write(page.extract_text() or "")
            for idx, table in enumerate(page.extract_tables() or [], start=1):
                with (tables_dir / f"page_{page_num:03d}_table_{idx:02d}.csv").open("w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(table)
    print(text_path)
    print(tables_dir)


def extract_sec_facts(args: argparse.Namespace) -> None:
    facts_path = Path(args.companyfacts)
    out_path = Path(args.out)
    tags = args.tags or ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "GrossProfit", "OperatingIncomeLoss", "NetIncomeLoss", "Assets", "Liabilities", "StockholdersEquity", "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment"]
    data = json.loads(facts_path.read_text(encoding="utf-8"))
    facts = data.get("facts", {}).get("us-gaap", {})
    rows: list[dict[str, str]] = []
    for tag in tags:
        item = facts.get(tag)
        if not item:
            continue
        for unit, observations in item.get("units", {}).items():
            for obs in observations:
                rows.append({"tag": tag, "label": item.get("label", ""), "unit": unit, "fy": str(obs.get("fy", "")), "fp": obs.get("fp", ""), "form": obs.get("form", ""), "filed": obs.get("filed", ""), "end": obs.get("end", ""), "frame": obs.get("frame", ""), "value": str(obs.get("val", "")), "accn": obs.get("accn", "")})
    ensure_dir(out_path.parent)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["tag", "label", "unit", "fy", "fp", "form", "filed", "end", "frame", "value", "accn"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(out_path)


def add_common_market_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--code", required=True)
    p.add_argument("--date-from", required=True, help="YYYYMMDD for HKEX, YYYY-MM-DD for CNINFO")
    p.add_argument("--date-to", required=True, help="YYYYMMDD for HKEX, YYYY-MM-DD for CNINFO")
    p.add_argument("--doc-type", default="annual", choices=["annual", "interim", "quarterly", "esg", "all"])
    p.add_argument("--limit", type=int, default=20)


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve and extract official financial filings")
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("hkex-search", help="Search HKEXnews filings by Hong Kong stock code")
    add_common_market_args(p)
    p.set_defaults(func=hkex_search)

    p = sub.add_parser("hkex-download-latest", help="Download latest HKEXnews filing by Hong Kong stock code")
    add_common_market_args(p)
    p.add_argument("--out", required=True)
    p.set_defaults(func=hkex_download_latest)

    p = sub.add_parser("cninfo-search", help="Search CNINFO filings by A-share stock code")
    add_common_market_args(p)
    p.set_defaults(func=cninfo_search)

    p = sub.add_parser("cninfo-download-latest", help="Download latest CNINFO filing by A-share stock code")
    add_common_market_args(p)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cninfo_download_latest)

    p = sub.add_parser("sec-submissions", help="Download SEC submissions JSON by CIK")
    p.add_argument("--cik", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=sec_submissions)

    p = sub.add_parser("sec-companyfacts", help="Download SEC XBRL companyfacts JSON by CIK")
    p.add_argument("--cik", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=sec_companyfacts)

    p = sub.add_parser("download", help="Download an official filing/document URL")
    p.add_argument("--url", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--filename")
    p.add_argument("--source-system")
    p.add_argument("--document-type")
    p.add_argument("--source-identifier")
    p.add_argument("--notes")
    p.set_defaults(func=download)

    p = sub.add_parser("extract-pdf", help="Extract page text and tables from a PDF")
    p.add_argument("--pdf", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=extract_pdf)

    p = sub.add_parser("extract-sec-facts", help="Flatten selected SEC companyfacts tags to CSV")
    p.add_argument("--companyfacts", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--tags", nargs="*")
    p.set_defaults(func=extract_sec_facts)

    args = parser.parse_args()
    if getattr(args, "func", None) in {cninfo_search, cninfo_download_latest} and args.doc_type == "esg":
        raise SystemExit("CNINFO does not support --doc-type esg in this command; use annual/interim/quarterly/all")
    args.func(args)


if __name__ == "__main__":
    main()
