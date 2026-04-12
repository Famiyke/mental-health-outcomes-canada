# Project 5: Provincial Mental Health Outcomes (CCHS PUMF)

**Domain:** Mental Health / Population Health
**Tools:** Python · SQL · Power BI
**Real Data Source:** Statistics Canada — CCHS Public Use Microdata File
**Download:** https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X
(Free — registration and user agreement required)

---

## Business Question
What is the prevalence of mental health conditions across provinces and demographic groups, what predicts perceived mental health status, and where should provincial mental health investment be directed?

---

## How to Get the Real CCHS Data
1. Go to: https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X
2. Create a free Statistics Canada account
3. Accept the user agreement
4. Download the PUMF CSV (CCHS_PUMF_Annual_Component.csv)
5. Download the data dictionary (codebook) alongside it
6. Rename: `cchs_pumf.csv` and place in this folder
7. Check the codebook to confirm variable names match constants in `simulate_cchs.py`

## How to Run (demo mode)
```bash
pip install pandas numpy
python simulate_cchs.py   # creates cchs_data.csv (~5,000 representative records)
python analysis.py        # full analysis — cleaning, prevalence, equity gaps, recommendations
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Decoded CCHS coded variables (e.g., income quintile, valid skip codes), recoded Likert scales, handled "not stated" response codes, validated provincial sample sizes |
| SQL/Python Programmer | Calculated prevalence rates by province, age, sex, income, and Indigenous identity; cross-tabulated risk factor combinations; identified highest-need subgroups |
| Dashboard Architect | Built Power BI dashboard with provincial map, demographic breakdowns, condition prevalence, and unmet need analysis |
| Data Storyteller | Produced a plain-language mental health equity brief for a provincial mental health director |
| Strategic Consultant | Identified three underserved groups for targeted provincial investment with specific program recommendations |

---

## Key Findings

1. **NB and NL rank lowest nationally for good mental health.** NB reports good/excellent mental health at 61.0% — the lowest of any province. NL follows at 62.2% and NS at 63.1%. All three sit below the national average of 66.8%. Atlantic provinces have a structural mental health access gap linked to limited psychiatrist supply and rural geography.

2. **Income is the strongest predictor of poor mental health.** Low-income respondents (under $30K) report good mental health at 51.7% — compared to 80.4% for those earning over $100K. Low-income respondents report poor mental health at 1.5x the national rate. The gap reflects both direct financial stress and reduced access to care.

3. **Indigenous unmet mental health need is 4.6x higher than non-Indigenous.** Indigenous respondents report good mental health at 54.6% versus 67.4% for non-Indigenous respondents — a 12.8 percentage point gap. Their unmet mental health need (53.8%) is 4.6x higher than non-Indigenous respondents (11.7%). This is the largest equity gap in the dataset.

4. **Anxiety overtook depression as the most prevalent condition.** Anxiety (12.0%) exceeds depression (9.4%) in this dataset, consistent with recent CCHS trend data showing anxiety disorders growing faster than any other mental health condition since 2015.

---

## Live Dashboard

Power BI dashboard built in Power BI Desktop.

**Download:** `mental_health_outcomes.pbix` from this repo and open in Power BI Desktop to interact with the full report.

**Dashboard pages:**
- Page 1 — National Snapshot: KPI cards, condition prevalence bar chart, unmet need gauge
- Page 2 — Provincial Analysis: filled map, province ranking, Atlantic focus
- Page 3 — Demographic Breakdown: income gradient, age group, sex comparison
- Page 4 — Equity Analysis: Indigenous gap, high-risk group, income × province matrix

See `powerbi_spec.md` for DAX measures and page-by-page build guide.

---

## Strategic Recommendations

1. **Atlantic access expansion.** NB, NL, and NS all rank in the bottom three nationally. Expand virtual mental health services with provincial health card coverage and remove referral gatekeeping for online CBT programs in these provinces.

2. **Low-income subsidised counselling.** Low-income respondents have the highest unmet need but the lowest provider contact rates. Community-based, subsidised counselling programs — not hospital referrals — are the right delivery model for this group.

3. **Indigenous-led mental health services.** The 4.6x unmet need gap between Indigenous and non-Indigenous respondents is the largest equity gap in the dataset. Provinces must fund Indigenous-led mental health services and honour existing UNDRIP commitments. Referrals to mainstream services are not sufficient.

4. **Anxiety-first CBT programs.** Anxiety disorders are now more prevalent than depression in this dataset. Structured online CBT programs with low-cost or no-cost access can serve mild-to-moderate anxiety cases before they escalate to crisis, reducing both suffering and system demand.

---

## Files

| File | Purpose |
|------|---------|
| `simulate_cchs.py` | Builds representative respondent-level data from published CCHS statistics — income-based probability model anchored to CCHS income quintile tables and First Nations supplement |
| `analysis.py` | National snapshot, province ranking, demographic breakdown, Indigenous gap, condition prevalence, high-risk group analysis, recommendations |
| `sql_queries.sql` | 8 SQL queries covering prevalence, province ranking, demographic breakdowns, Indigenous gap, and equity analysis |
| `mental_health_outcomes.pbix` | Power BI dashboard — download and open in Power BI Desktop |
| `powerbi_spec.md` | Power BI build guide with DAX measures for all 4 dashboard pages |
| `equity_brief.md` | Plain-language mental health equity brief for a provincial director |

---

## Data Note
Statistics Canada CCHS PUMF microdata is available free with registration. Individual respondent data requires signing a user agreement. This project uses simulated data built with an income-based probability model anchored to published CCHS prevalence statistics. All source figures are documented inline in `simulate_cchs.py`.

---

## Dashboard Screenshots
![National Snapshot](screenshot_page1_national_snapshot.png)
![Provincial Analysis](screenshot_page2_provincial_analysis.png)
![Demographic Breakdown](screenshot_page3_demographic_breakdown.png)
![Equity Analysis](screenshot_page4_equity_analysis.png)
