"""
Project 5 – simulate_cchs.py
Builds a representative respondent-level dataset
modeled on Statistics Canada CCHS PUMF microdata.
~5,000 synthetic respondents matching published CCHS prevalence figures.
Real data: https://www150.statcan.gc.ca/n1/en/catalogue/82M0013X
"""

import pandas as pd
import numpy as np

np.random.seed(5)
N = 5000

PROVINCES = {
    "BC":0.130,"AB":0.110,"SK":0.030,"MB":0.035,
    "ON":0.385,"QC":0.235,"NB":0.022,"NS":0.026,"PE":0.004,"NL":0.023
}

AGE_GROUPS = {"18-34":0.27,"35-49":0.25,"50-64":0.24,"65+":0.24}

# Published CCHS mental health good/excellent prevalence by province (%)
# Source: Statistics Canada CCHS 2022 Public Summary
GOOD_MENTAL_HEALTH = {
    "BC":0.73,"AB":0.74,"SK":0.72,"MB":0.70,"ON":0.72,
    "QC":0.73,"NB":0.67,"NS":0.68,"PE":0.69,"NL":0.66,
}

# Chronic condition prevalence (from CCHS published tables)
CHRONIC_PREV = {
    "Depression":      0.12,
    "Anxiety":         0.10,
    "PTSD":            0.04,
    "Bipolar":         0.02,
    "Substance_Use":   0.08,
}

# Generate respondents
prov_list  = np.random.choice(list(PROVINCES.keys()), N,
                               p=list(PROVINCES.values()))
age_list   = np.random.choice(list(AGE_GROUPS.keys()), N,
                               p=list(AGE_GROUPS.values()))
sex_list   = np.random.choice(["Male","Female"], N, p=[0.48,0.52])
income_list = np.random.choice(
    ["< $30K","$30K–$60K","$60K–$100K","$100K+"], N,
    p=[0.22, 0.31, 0.27, 0.20]
)
edu_list    = np.random.choice(
    ["Less than HS","High School","Some Post-Sec","University+"], N,
    p=[0.12, 0.22, 0.28, 0.38]
)
indigenous_list = np.random.choice(["Yes","No"], N, p=[0.05, 0.95])

# Mental health outcome — good/excellent perceived mental health
good_mh = np.array([
    np.random.random() < GOOD_MENTAL_HEALTH[p] for p in prov_list
])

# Self-rated mental health (1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor)
mh_rating = np.where(
    good_mh,
    np.random.choice([1, 2, 3], N, p=[0.25, 0.45, 0.30]),
    np.random.choice([3, 4, 5], N, p=[0.20, 0.45, 0.35])
)

# Chronic conditions — correlated with poor mental health
records = []
for i in range(N):
    poor_mh_mult = 1.0 if good_mh[i] else 2.8
    age_mult = {"18-34":1.1,"35-49":1.0,"50-64":0.85,"65+":0.70}[age_list[i]]
    income_mult = {"< $30K":1.6,"$30K–$60K":1.1,"$60K–$100K":0.95,"$100K+":0.80}[income_list[i]]

    conditions = {
        cond: int(np.random.random() < prev * poor_mh_mult * age_mult * income_mult)
        for cond, prev in CHRONIC_PREV.items()
    }

    records.append({
        "respondent_id":   i + 1,
        "province":        prov_list[i],
        "age_group":       age_list[i],
        "sex":             sex_list[i],
        "income_group":    income_list[i],
        "education":       edu_list[i],
        "indigenous":      indigenous_list[i],
        "mh_rating":       mh_rating[i],
        "good_mh":         int(good_mh[i]),
        **conditions,
        "has_any_condition": int(any(conditions.values())),
        "unmet_need":      int(np.random.random() < (0.06 if good_mh[i] else 0.28)),
        "saw_mh_provider": int(np.random.random() < (0.10 if good_mh[i] else 0.35)),
    })

df = pd.DataFrame(records)
df.to_csv("cchs_data.csv", index=False)
print(f"Created cchs_data.csv  —  {len(df):,} respondents")
print(f"Columns: {list(df.columns)}")
print(f"\nPublished CCHS check — good mental health rate:")
for prov in sorted(GOOD_MENTAL_HEALTH.keys()):
    simulated = df[df["province"] == prov]["good_mh"].mean()
    published = GOOD_MENTAL_HEALTH[prov]
    print(f"  {prov}: simulated {simulated:.2f}  published {published:.2f}")
