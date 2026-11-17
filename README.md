# Project 5: Synthetic Mental Health Outcomes Analytics

> **DATA PROVENANCE:** This portfolio project uses simulated records informed by named Canadian public sources. All generated statistics, rankings, demographic differences, and savings models are illustrative rather than verified official estimates. Recommendations are hypothetical scenarios, not observed effects.

**Domain:** Mental Health / Population Health
**Tools:** Python · SQL · Power BI
**Public reference source (distinct from simulated analysis data):** Statistics Canada — CCHS Public Use Microdata File
**Download:** https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X
(Free — registration and user agreement required)

---

## Business Question
How can an analyst build and quality-check a mental health reporting workflow, including stratified indicators, suppression of small groups, and responsible interpretation?

---

## Official reference data for a separate, validated study
1. Go to: https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X
2. Create a free Statistics Canada account
3. Accept the user agreement
4. Download the PUMF CSV (CCHS_PUMF_Annual_Component.csv)
5. Download the data dictionary (codebook) alongside it
6. Rename: `cchs_pumf.csv` and place in this folder
7. Build a separate import, variable mapping and survey-weighted analysis workflow. `simulate_cchs.py` does not load or analyze the CCHS PUMF.

## How to Run (demo mode)
```bash
pip install pandas numpy
python simulate_cchs.py   # creates cchs_data.csv (5,000 generated records)
python analysis.py        # full analysis — cleaning, prevalence, equity gaps, recommendations
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Validated generated indicator categories, checked missingness and compared simulated subgroup sample sizes |
| SQL/Python Programmer | Calculated prevalence rates by province, age, sex, income, and Indigenous identity; cross-tabulated risk factor combinations; identified highest-need subgroups |
| Dashboard Architect | Built Power BI dashboard with provincial map, demographic breakdowns, condition prevalence, and unmet need analysis |
| Data Storyteller | Produced a plain-language mental health equity brief for a provincial mental health director |
| Reporting and interpretation | Documented limitations, denominator checks and minimum subgroup sample-size requirements |

---

## Illustrative analytical outputs

This project's Python/SQL outputs illustrate data processing, comparisons, modeling and reporting using generated records. The specific rates, rankings, cost figures and trends in the demonstration are **not verified official findings**. See the analysis scripts for the computations and the data limitations section below for interpretation requirements.

## Power BI demonstration status

**Historical PBIX file, not validated for public statistics.** The current `mental_health_outcomes.pbix` still holds an older generated dataset and misleading source labels. It has not yet been refreshed with the corrected generator. Do not use its figures or report pages as evidence of actual population disparities.

The corrected Python generator and analysis code are the authoritative reproducible demonstration. See [DASHBOARD_CORRECTION_GUIDE.md](DASHBOARD_CORRECTION_GUIDE.md) for exact Power BI Desktop fixes required before the historical report is suitable to showcase. Existing screenshots are retained as historical QA evidence but are not presented here as validated outputs.

## Interpretation and real-world next steps

Use the simulated findings to demonstrate analytical methods, not to rank actual jurisdictions or recommend clinical or policy interventions. A real decision requires matched official data, documented definitions, relevant uncertainty, and clinical or operational stakeholder review. Financial scenarios must include assumptions, costs and sensitivity analysis.

## Files

| File | Purpose |
|------|---------|
| `simulate_cchs.py` | Builds representative respondent-level data from published CCHS statistics — income-based probability model anchored to CCHS income quintile tables and First Nations supplement |
| `analysis.py` | National snapshot, province ranking, demographic breakdown, Indigenous gap, condition prevalence, high-risk group analysis, recommendations |
| `sql_queries.sql` | 8 SQL queries covering prevalence, province ranking, demographic breakdowns, Indigenous gap, and equity analysis |
| `mental_health_outcomes.pbix` | Power BI dashboard — download and open in Power BI Desktop |
| `dashboard.md` | Power BI build guide with DAX measures for all 4 dashboard pages |
| `equity_brief.md` | Plain-language mental health equity brief for a provincial director |

---

## Data Provenance and Limitations

The respondent records are simulated, not actual CCHS PUMF respondents. Provincial, income, and Indigenous identity comparisons are illustrative, not survey estimates. They must not be generalized without actual survey weights, variance calculations, and careful validation of geography and population coverage.

Statistics Canada CCHS PUMF microdata is available free with registration. Individual respondent data requires signing a user agreement. This project uses simulated data built with an income-based probability model anchored to published CCHS prevalence statistics. All source figures are documented inline in `simulate_cchs.py`.

---

## Historical dashboard screenshots

Screenshots remain in the repository for issue tracking. They are not displayed here because the associated PBIX needs updated data, source captions, small-cell suppression and a visible simulated-data banner.

---

## Reproducibility and execution status

**Environment:** Python 3 with `pandas` and `numpy` installed. If working with the Excel files, install `openpyxl` as needed. Run the simulation script before the analysis commands shown above.

**Important:** The scripts are designed for the generated datasets and expected column names. Downloading a public government table does **not** guarantee that it will run with these scripts unchanged; a schema-mapping and validation step is required for authentic external data. Automated GitHub Actions tests have successfully executed the generated-data Python workflow. Independent reconciliation against actual Statistics Canada data has not been completed.

