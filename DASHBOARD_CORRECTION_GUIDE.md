# Power BI dashboard correction specification

**Status: The PBIX is structurally readable, but must not be presented as an official CCHS report.** The four page screenshots and the PBIX layout were inspected on 17 November 2026.

## Required corrections in Power BI Desktop

1. Put a high-contrast banner at the top of **every page**: **SIMULATED DATA — DEMONSTRATION ONLY. NOT STATISTICS CANADA CCHS RESULTS.**
2. Replace the National Snapshot footer **"Source: Statistics Canada CCHS | 5,000 respondents | All province"** with **"Source: Generated 5,000-record demonstration dataset; CCHS cited for background only."** Do not identify simulated persons as actual respondents.
3. National Snapshot: The **Good MH 66.8** and **Poor MH 26.4** figures total 93.2%, not 100%. A two-segment donut normalizes them and may mislead users. Verify the denominator, document any missing/other category, and use a stacked bar or a complete 100% composition only if categories are exhaustive and mutually exclusive.
4. Equity Analysis: Replace **"Indigenous unmet need ratio 4.6 times higher"** with an illustrative ratio label, and add explicit text that synthetic modeled differences are **not observed Indigenous population estimates**. Avoid policy conclusions from this simulated model.
5. Provincial Analysis: PE has only **23 simulated respondents** in the shown scorecard. Do not rank small groups as comparable provincial population estimates. Apply a minimum sample-size rule consistently, or suppress unstable cells.
6. Equity Analysis: The province-by-income table displays **100.00%** in some small simulated subgroups. Suppress or clearly flag small cells, rather than relying only on a footnote that n under 20 should be interpreted with caution.
7. Label every chart with units: percentages vs raw counts, the base used, and the simulation reference period.
8. Validate DAX calculations and visual filters using a data dictionary with explicit field names, numerator, denominator, and handling of missing responses.
9. Reopen and test the revised PBIX in Power BI Desktop. Take screenshots of all four updated report pages. The edited PBIX should replace the repository file only after opening without errors.

## Validation boundary

This review verified that the PBIX contains four pages and that the supplied screenshots visibly show charts. It did not independently test DAX execution in Power BI Desktop or establish representative survey estimates.

Use official Statistics Canada microdata, weighted analysis, variance methodology and appropriate community governance before reporting actual survey findings.
