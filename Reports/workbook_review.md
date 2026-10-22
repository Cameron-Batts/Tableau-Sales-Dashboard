# Packaged Tableau Workbook Review

**Report review and documentation:** Cameron Batts

## Workbooks now included

| Package | Embedded source | Definition checks |
| --- | --- | --- |
| Executive-Sales-Metrics.twbx | Separate Sample - Superstore Hyper extract | Two dashboards, 23 worksheets and nine declared actions |
| Sales-Customer-Analytics.twbx | Orders + Manager Hyper extract | One dashboard, one story and 14 worksheets; no workbook-level action definitions |

The supplied Excel-backed V1 and V2 variants were also inspected for comparison. Their embedded spreadsheet exactly matches the uploaded sales spreadsheet. The two Public variants above are preserved byte-for-byte from the supplied packages; their internal workbook definitions and data have not been rewritten. The original educational file titles are source lineage, not evidence that all workbook elements were newly authored for this review.

## Confirmed calculations

- Executive Profit Ratio: `SUM(Profit) / SUM(Sales)`.
- Executive customers and orders use distinct-count fields in the workbook definitions.
- Sales Profit Margin G: `SUM(Profit) / SUM(Sale Amount)`. The separate row-level Profit Margin B is `Profit / Sale Amount`; averaging row ratios is not the same as the aggregate margin.
- Days to Ship: `DATEDIFF('day', Order Date, Ship Date)`.
- V2 Shipping Target defaults to 3 days. Shipping Target Met compares the average Days to Ship at the current view grain with that parameter; a mean above 3 is labeled Problem. This is not an order-level on-time delivery rate. V1 defaults to 5 days, so versions have different thresholds.
- The executive workbook declares category, timeline, heatmap and map filter/highlight actions. Presence in XML does not establish that each action works when clicked.
- The executive Order Date (anchored) calculation shifts dates relative to `TODAY()`. Its displayed relative dates can change when reopened and do not represent refreshed transactions.

## Why the headline totals differ

The executive package uses its own Sample - Superstore extract; the sales package uses Orders + Manager. They are separate sources. The executive preview's approximately $8.952M sales and the included spreadsheet's approximately $2.327M sales should not be reconciled as if they came from one population. The new files identify the source distinction. The exact executive KPI values and filter state still require an extract query or a Tableau run.

## Verification and limits

All four uploaded packages passed ZIP integrity checks and their `.twb` XML parsed successfully. The two packaged public variants now included in the project contain their referenced Hyper extracts. The source spreadsheet's totals were independently recomputed with `Analysis/verify_sales.py`. Workbook structure, formulas, parameters and declared actions were inspected with `Analysis/inspect_workbooks.py`.

A Hyper API query was attempted but could not start because the environment blocked its required local socket. No embedded-extract query, refresh test or calculation-engine equivalence test succeeded in that automated environment. The owner subsequently reported successful manual loading and basic interaction checks for the sales workbook. Static definition inspection is not a full runtime validation.

## Owner-reported Tableau checks

On October 22, 2026, Cameron reported that Sales-Customer-Analytics.twbx opened normally in Tableau, filters updated charts and totals, clearing a filter restored the original view, tooltips displayed correctly, and chart selections behaved as expected. These are owner-reported manual checks, not independently observed runtime tests. Executive-Sales-Metrics.twbx, data refresh, embedded-extract queries and reconciliation of displayed KPI totals remain unverified.

## Reproduce

```bash
python Analysis/inspect_workbooks.py
python Analysis/verify_sales.py
```

Install the dependencies in `requirements.txt` before the spreadsheet check. To review the dashboards visually, open the packaged workbooks in a compatible Tableau application; they were saved by Tableau 2025.3.1. Native application compatibility has not been tested here.
