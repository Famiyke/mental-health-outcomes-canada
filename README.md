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
pip install pandas numpy openpyxl
python simulate_cchs.py     # creates cchs_data.csv (~5000 representative records)
python 01_clean_explore.py  # data detective
python 02_analysis.py       # full analysis
```

---

## Analyst Roles

| Hat | What I Did |
|-----|-----------|
| Data Detective | Decoded CCHS coded variables (e.g., sex: 1=Male, 2=Female), recoded Likert scales, handled "valid skip" and "not stated" response codes |
| SQL/Python Programmer | Calculated weighted prevalence rates, cross-tabulated by age/sex/income, identified risk factor combinations |
| Dashboard Architect | Built Power BI dashboard with demographic breakdowns and geographic distribution |
| Data Storyteller | Produced a plain-language mental health equity brief |
| Strategic Consultant | Identified three underserved groups for targeted provincial investment |

---

## Files

| File | Purpose |
|------|---------|
| `simulate_cchs.py` | Builds representative respondent-level data from published CCHS statistics |
| `01_clean_explore.py` | Decode variables, handle special codes, profile — Data Detective |
| `02_analysis.py` | Prevalence by group, risk factor analysis, geographic gaps |
| `sql_queries.sql` | All key queries in SQL |
| `powerbi_spec.md` | Power BI dashboard guide with mental health DAX measures |
| `equity_brief.md` | One-page equity brief for a provincial mental health director |
