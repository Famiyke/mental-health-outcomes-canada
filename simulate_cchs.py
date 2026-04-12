"""
Project 5 – simulate_cchs.py
Builds a representative respondent-level dataset
modeled on Statistics Canada CCHS PUMF microdata.
~5,000 synthetic respondents anchored to published CCHS prevalence figures.
Real data: https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X

Simulation model:
- Income-based probability as primary driver of good MH
  (anchored to published CCHS income quintile tables)
- Province modifier applied as secondary adjustment
  (anchored to CCHS 2022 provincial good/excellent MH summary)
- Indigenous adjustment of -14pp
  (anchored to CCHS First Nations supplement)
- Unmet need: 4x higher for Indigenous respondents,
  1.6x higher for low income
"""

import pandas as pd
import numpy as np

np.random.seed(77)
N = 5000

PROVINCES = {
    "BC":0.130, "AB":0.110, "SK":0.030, "MB":0.035, "ON":0.385,
    "QC":0.235, "NB":0.022, "NS":0.026, "PE":0.004, "NL":0.023,
}

# Province modifiers — relative to national average
# Source: Statistics Canada CCHS 2022 Public Summary
PROV_MOD = {
    "BC":+0.02, "AB":+0.03, "SK":+0.01, "MB":-0.01, "ON":+0.01,
    "QC":+0.02, "NB":-0.06, "NS":-0.04, "PE":-0.02, "NL":-0.05,
}

# Income-based good MH base probability
# Source: CCHS published income quintile tables (lowest quintile ~52%, highest ~80%)
INC_BASE = {
    "< $30K":     0.52,
    "$30K-$60K":  0.64,
    "$60K-$100K": 0.72,
    "$100K+":     0.80,
}

AGE_GROUPS = {"18-34":0.27, "35-49":0.25, "50-64":0.24, "65+":0.24}

prov_list  = np.random.choice(list(PROVINCES.keys()), N, p=list(PROVINCES.values()))
inc_list   = np.random.choice(list(INC_BASE.keys()),  N, p=[0.22, 0.31, 0.27, 0.20])
indig_list = np.random.choice(["Yes","No"],            N, p=[0.05, 0.95])
edu_list   = np.random.choice(
    ["Less than HS","High School","Some Post-Sec","University+"],
    N, p=[0.12, 0.22, 0.28, 0.38]
)
age_list   = np.random.choice(list(AGE_GROUPS.keys()), N, p=list(AGE_GROUPS.values()))
sex_list   = np.random.choice(["Male","Female"],        N, p=[0.48, 0.52])

records = []
for i in range(N):
    # Base probability from income, adjusted by province and Indigenous identity
    prob = INC_BASE[inc_list[i]] + PROV_MOD[prov_list[i]]
    if indig_list[i] == "Yes":
        prob -= 0.14   # Indigenous adjustment (CCHS First Nations supplement)
    prob = max(0.20, min(0.95, prob + np.random.normal(0, 0.03)))
    good_mh = int(np.random.random() < prob)

    # Unmet need — Indigenous 4x, low income 1.6x
    base_unmet = 0.05 if good_mh else 0.22
    if indig_list[i] == "Yes":  base_unmet *= 4.0
    if inc_list[i] == "< $30K": base_unmet *= 1.6
    unmet = int(np.random.random() < min(0.95, base_unmet))

    # Chronic conditions — correlated with poor MH
    anxiety    = int(np.random.random() < (0.22 if not good_mh else 0.07))
    depression = int(np.random.random() < (0.18 if not good_mh else 0.05))
    ptsd       = int(np.random.random() < (0.08 if not good_mh else 0.02))
    bipolar    = int(np.random.random() < (0.04 if not good_mh else 0.01))
    substance  = int(np.random.random() < (0.14 if not good_mh else 0.04))

    mh_rating = (
        np.random.choice([1,2,3], p=[0.25,0.45,0.30]) if good_mh
        else np.random.choice([3,4,5], p=[0.20,0.45,0.35])
    )

    records.append({
        "respondent_id":    i + 1,
        "province":         prov_list[i],
        "age_group":        age_list[i],
        "sex":              sex_list[i],
        "income_group":     inc_list[i],
        "education":        edu_list[i],
        "indigenous":       indig_list[i],
        "mh_rating":        mh_rating,
        "good_mh":          good_mh,
        "unmet_need":       unmet,
        "saw_mh_provider":  int(np.random.random() < (0.35 if not good_mh else 0.10)),
        "Depression":       depression,
        "Anxiety":          anxiety,
        "PTSD":             ptsd,
        "Bipolar":          bipolar,
        "Substance_Use":    substance,
        "has_any_condition": int(any([depression, anxiety, ptsd, bipolar, substance])),
    })

df = pd.DataFrame(records)
df.to_csv("cchs_data.csv", index=False)
print(f"Created cchs_data.csv  —  {len(df):,} respondents")
print(f"Columns: {list(df.columns)}")

# Verification summary
nat     = df.good_mh.mean()*100
low_p   = (1 - df[df.income_group=="< $30K"].good_mh.mean())*100
nat_p   = (1 - df.good_mh.mean())*100
iu      = df[df.indigenous=="Yes"].unmet_need.mean()*100
nu      = df[df.indigenous=="No"].unmet_need.mean()*100
ig      = df[df.indigenous=="Yes"].good_mh.mean()*100
ng      = df[df.indigenous=="No"].good_mh.mean()*100
anx     = df.Anxiety.mean()*100
dep     = df.Depression.mean()*100
nb      = df[df.province=="NB"].good_mh.mean()*100
nl      = df[df.province=="NL"].good_mh.mean()*100

print(f"\nNational good MH:       {nat:.1f}%")
print(f"NB: {nb:.1f}%  NL: {nl:.1f}%  (both below national avg: {nb<nat and nl<nat})")
print(f"Low-income poor MH ratio: {low_p:.1f}/{nat_p:.1f} = {low_p/nat_p:.1f}x")
print(f"Indigenous unmet ratio:   {iu:.1f}/{nu:.1f} = {iu/nu:.1f}x")
print(f"Indigenous good MH gap:   {ig:.1f}% vs {ng:.1f}% ({ng-ig:.1f}pp gap)")
print(f"Anxiety {anx:.1f}% > Depression {dep:.1f}%: {anx>dep}")
