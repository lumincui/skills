---
name: official-financial-filings
description: Retrieve first-party company financial filings and extract audited/source-backed financial data. Use when asked to get latest financial statements, annual reports, interim reports, earnings releases, revenue/profit figures, SEC filings, HKEX filings, A-share announcements, exchange disclosures, or when any analysis requires current financial statement, revenue, earnings, margin, balance sheet, cash flow, or profitability data. Always determine listing venue first, use official exchange/regulator/company IR sources, preserve source links, and query live/current data instead of relying on memory or stale knowledge.
---

# Official Financial Filings

## Non-negotiable rule

When a user asks for financial statement data, revenue, profit, margin, EPS, balance sheet, cash flow, guidance, or valuation inputs tied to reported financials, **query the latest available source in real time** before answering or modeling. Do not rely on memory, training data, prior conversation, or stale downloaded files unless the user explicitly asks for a historical archived copy.

Use first-party sources only for raw financial data: connected institutional MCPs, SEC EDGAR, HKEXnews, CNINFO, official exchange/regulator portals, or company IR supplements. Never use general web-search snippets as the source of financial figures; search may only locate official pages.

## Quick commands

Run commands from the skill directory or use an absolute path to `scripts/filing_tools.py`.

### Hong Kong H-shares / HKEXnews

Search filings:

```bash
python scripts/filing_tools.py hkex-search --code 02338 --date-from 20250101 --date-to 20260518 --doc-type annual
```

Download the latest filing from the search result:

```bash
python scripts/filing_tools.py hkex-download-latest --code 02338 --date-from 20250101 --date-to 20260518 --doc-type annual --out filings/weichai_h
```

`--doc-type` values: `annual`, `interim`, `quarterly`, `esg`, `all`.

Important: HKEX search uses an internal `stockId`; do not pass the displayed stock code as `stockId`. The script resolves the stock code through HKEX active stock JSON first.

### China A-share / CNINFO

Search filings:

```bash
python scripts/filing_tools.py cninfo-search --code 000338 --date-from 2025-01-01 --date-to 2026-05-18 --doc-type annual
```

Download the latest filing from the search result:

```bash
python scripts/filing_tools.py cninfo-download-latest --code 000338 --date-from 2025-01-01 --date-to 2026-05-18 --doc-type annual --out filings/weichai_a
```

`--doc-type` values: `annual`, `interim`, `quarterly`, `all`.

The script infers CNINFO column from stock code: `60/68` → SSE, `00/30` → SZSE, `43/83/87/92` → BSE.

### US / SEC EDGAR

```bash
python scripts/filing_tools.py sec-submissions --cik 0000320193 --out filings/apple
python scripts/filing_tools.py sec-companyfacts --cik 0000320193 --out filings/apple
python scripts/filing_tools.py extract-sec-facts --companyfacts filings/apple/sec_companyfacts_CIK0000320193.json --out filings/apple/facts.csv
```

### PDF extraction

```bash
python scripts/filing_tools.py extract-pdf --pdf filings/company/report.pdf --out filings/company/extracted
```

If `pdfplumber` is missing:

```bash
python -m pip install pdfplumber
```

## Workflow

1. Identify listing venue from ticker suffix or stock code.
2. Run the relevant official-source command above.
3. Download and preserve the original file before extracting data.
4. Extract tables/text only from the downloaded official file.
5. Cite every number with source system, filing title, filing date, URL/local path, and page/table/XBRL tag when available.
6. State “latest checked through” date and source in the final answer.

## Source log

Each download writes `source_log.csv` with: company name, ticker/code, listing venue, source system, document type, filing date, source URL, source identifier, local path, retrieval timestamp, and notes.

## Data extraction rules

- Prefer structured data when available: SEC XBRL/companyfacts, official Excel supplements, inline XBRL.
- For HKEXnews and CNINFO PDFs, extract page text/tables and manually sanity-check key numbers against the original page.
- Separate reported GAAP/IFRS figures from adjusted/non-GAAP figures.
- Preserve original units and currency; convert only in a separate derived column.
- Do not mix periods in numerator/denominator without explicit disclosure.
- Use company fiscal period labels, not calendar guesses.
- Never invent missing values. If a value cannot be found, write `Not disclosed` with the source checked.
- For private companies, do not present media-reported revenue/valuation as audited financials.
