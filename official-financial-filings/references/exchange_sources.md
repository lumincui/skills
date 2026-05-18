# Official filing sources

Use this reference when choosing the first-party source for raw financial filings.

| Market | Official source | Best documents | Notes |
|---|---|---|---|
| US | SEC EDGAR | 10-K, 10-Q, 8-K earnings release, S-1, DEF 14A, XBRL/companyfacts | Best structured data availability. Use CIK and accession numbers. |
| Hong Kong | HKEXnews | Annual report, interim report, annual/interim results, announcements, prospectus | PDFs/HTML. Use stock code and announcement category. |
| China A-share | CNINFO, SSE, SZSE, BSE | Annual report, interim report, quarterly report, announcements | CNINFO is usually the broadest disclosure portal. |
| UK | LSE RNS, FCA NSM, Companies House | Annual report, preliminary results, interim results | Companies House filings may lag market announcements. |
| EU | National storage mechanism / exchange | Annual and interim financial reports | Source varies by country. |
| Japan | EDINET, TDnet | Securities reports, quarterly reports, timely disclosure | EDINET has statutory filings; TDnet has timely announcements. |
| Singapore | SGXNet | Annual report, financial statements, announcements | Official SGX disclosure platform. |
| Canada | SEDAR+ | Annual/interim filings, MD&A, prospectus | Official Canadian issuer disclosure system. |
| Australia | ASX announcements | Annual report, half-year report, Appendix 4E/4D | Official ASX announcements portal. |
| Private companies | Company releases, investor releases, official pricing pages, procurement databases, corporate registry filings where applicable | Usually no full audited public financials | Label missing/non-audited data clearly. |

## Filing selection priority

1. Latest full-year audited annual report / 10-K.
2. Latest interim/quarterly filing / 10-Q.
3. Latest results announcement or earnings release if newer than the report.
4. Financial supplement or investor presentation for segment/non-GAAP detail.
5. Earnings call transcript for qualitative context only unless management gives explicit metrics.

## Source log minimum schema

- company_name
- ticker_or_code
- listing_venue
- source_system
- document_type
- fiscal_period
- filing_or_announcement_date
- source_url
- source_identifier
- local_path
- retrieved_at
- notes
