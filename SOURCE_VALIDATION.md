# Source validation boundary

Statistics Canada's Canadian Community Health Survey PUMF requires survey weights for representative population tabulations. The official CCHS user guidance warns that unweighted estimates do not reproduce the surveyed population.

Relevant source guidance: https://www.statcan.gc.ca/en/statistical-programs/document/3226_D7_T9_V3-eng.pdf

The respondent records in this project are **synthetically generated**, not CCHS respondents. Reported prevalence by province, income or Indigenous identity, as well as unmet-need ratios, are illustrative only. For defensible CCHS estimates, retrieve a specific PUMF edition, map questionnaire items to codebook variables, use the supplied sampling weights, address design-based uncertainty and disclosure rules, and consult applicable Indigenous data-governance principles.

**Validation status:** Survey-weighting requirement confirmed from Statistics Canada; project population results not verified and PBIX calculations not reconciled.
## Corrected analytical generator (17 November 2026)

The current `simulate_cchs.py` no longer imposes a fourfold Indigenous unmet-need multiplier or a negative Indigenous mental-health probability modifier. Those were unsupported synthetic assumptions that created a misleading modeled disparity. Rating categories are now exhaustive, the `good_mh` indicator derives consistently from ratings 1–3, and `validate_demo.py` checks their denominators. The analytics script no longer prints identity-comparison findings or unqualified percentages for provinces with fewer than 30 modeled records.

**Critical version boundary:** The checked-in `mental_health_outcomes.pbix` and older screenshot PNGs have **not been rebuilt** from the corrected generator. They retain the previous, invalid demonstration values and must not be presented as current results until replaced through Power BI Desktop.
