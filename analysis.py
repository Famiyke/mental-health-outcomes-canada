"""
Project 5 – analysis.py
Data Detective → Programmer → Storyteller → Consultant
Mental Health Outcomes — Synthetic Demo
"""

# PORTFOLIO DATA NOTICE: All computed findings below use simulated/generated
# analytical records, not verified official Canadian statistics. Numeric outputs
# illustrate methods only; any program recommendations require source validation.

import pandas as pd
import numpy as np

df  = pd.read_csv("cchs_data.csv")
sep = "=" * 62

print(f"\n{sep}")
print("  PROJECT 5 — SYNTHETIC MENTAL HEALTH OUTCOMES")
print(f"{sep}")

# ── Profile ───────────────────────────────────────────────────────────────────
print(f"\n  Generated records: {len(df):,}")
print(f"  Provinces:   {sorted(df['province'].unique())}")
print(f"  Age groups:  {sorted(df['age_group'].unique())}")

# Decode MH rating scale
mh_map = {1:"Excellent",2:"Very Good",3:"Good",4:"Fair",5:"Poor"}
df["mh_label"] = df["mh_rating"].map(mh_map)
df["good_mh"] = df["mh_rating"].isin([1,2,3]).astype(int)
df["poor_mh"] = df["mh_rating"].isin([4,5]).astype(int)
assert ((df["good_mh"] + df["poor_mh"]) == 1).all(), "Mental-health ratings must be exhaustive"

# ── National Snapshot ─────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("NATIONAL MENTAL HEALTH SNAPSHOT")
print(f"{'─'*62}")

good_pct  = df["good_mh"].mean() * 100
poor_pct  = df["poor_mh"].mean() * 100
unmet_pct = df["unmet_need"].mean() * 100
any_cond  = df["has_any_condition"].mean() * 100

print(f"\n  Good/Very good/Excellent MH:   {good_pct:.1f}%")
print(f"  Fair/Poor mental health:        {poor_pct:.1f}%")
print(f"  Unmet mental health need:       {unmet_pct:.1f}%")
print(f"  Have at least one condition:    {any_cond:.1f}%")
assert abs(good_pct + poor_pct - 100.0) < 1e-9, "Category percentages must sum to 100%"

# ── Province Ranking ──────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("SIMULATED PROVINCE COMPARISON — Good or Better Mental Health")
print(f"{'─'*62}")

prov = (df.groupby("province")
          .agg(good_mh=("good_mh","mean"),
               poor_mh=("poor_mh","mean"),
               unmet=("unmet_need","mean"),
               n=("respondent_id","count"))
          .sort_values("good_mh", ascending=False).reset_index())

nat_avg = df["good_mh"].mean()
print(f"\n  {'Province':>10} {'Good MH%':>10} {'Fair/Poor%':>12} {'Unmet Need%':>13} {'n':>5}")
print(f"  {'─'*10} {'─'*10} {'─'*12} {'─'*13} {'─'*5}")
for _, r in prov.iterrows():
    if r["n"] < 30:
        print(f"  {r['province']:>10}  SUPPRESSED: fewer than 30 synthetic records (n={int(r['n'])})")
        continue
    below = " ◄ BELOW SIMULATED AVG" if r["good_mh"] < nat_avg else ""
    print(f"  {r['province']:>10} {r['good_mh']:>9.1%} {r['poor_mh']:>11.1%}"
          f" {r['unmet']:>12.1%} {r['n']:>5,}{below}")

# ── Demographic Groups ────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("GOOD MENTAL HEALTH BY AGE GROUP")
print(f"{'─'*62}")

age = (df.groupby("age_group")["good_mh"].mean()
         .sort_values().reset_index())
print()
for _, r in age.iterrows():
    bar = "█" * int(r["good_mh"] * 30)
    print(f"  {r['age_group']:>8}  {r['good_mh']:>5.1%}  {bar}")

print(f"\n{'─'*62}")
print("GOOD MENTAL HEALTH BY INCOME GROUP")
print(f"{'─'*62}")

inc = (df.groupby("income_group")["good_mh"].mean()
         .reset_index().sort_values("good_mh"))
print()
for _, r in inc.iterrows():
    bar = "█" * int(r["good_mh"] * 30)
    print(f"  {r['income_group']:>15}  {r['good_mh']:>5.1%}  {bar}")

# ── Ethical handling of simulated demographic labels ─────────────────────────
print(f"\\n{'─'*62}")
print("DEMOGRAPHIC DATA LIMITATION")
print(f"{'─'*62}")
print("Identity-based comparisons are not presented as population disparities.")
print("Synthetic labels are not survey-weighted or suitable for policy inference.")

# ── Condition Prevalence ──────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("CHRONIC CONDITION PREVALENCE")
print(f"{'─'*62}")

conds = ["Depression","Anxiety","PTSD","Bipolar","Substance_Use"]
print(f"\n  {'Condition':<20} {'Prevalence':>12} {'Unmet Need%':>13}")
print(f"  {'─'*20} {'─'*12} {'─'*13}")
for cond in conds:
    prev  = df[cond].mean()
    unmet = df[df[cond] == 1]["unmet_need"].mean()
    print(f"  {cond:<20} {prev:>11.1%} {unmet:>12.1%}")

# ── Risk Factor Combinations ──────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("HIGH-RISK GROUP: Low Income + No Post-Secondary + Poor MH")
print(f"{'─'*62}")

low_income_no_edu = df[
    (df["income_group"] == "< $30K") &
    (df["education"].isin(["Less than HS","High School"]))
]
high_risk_rate = low_income_no_edu["poor_mh"].mean()
unmet_hr       = low_income_no_edu["unmet_need"].mean()
saw_provider   = low_income_no_edu["saw_mh_provider"].mean()
n_hr           = len(low_income_no_edu)

print(f"\n  High-risk respondents:  {n_hr:,} ({n_hr/len(df):.1%} of sample)")
print(f"  Fair/Poor mental health: {high_risk_rate:.1%}")
print(f"  Unmet mental health need:{unmet_hr:.1%}")
print(f"  Saw a MH provider:       {saw_provider:.1%}")

# ── Recommendations ───────────────────────────────────────────────────────────
print("\nILLUSTRATIVE INTERPRETATION AND NEXT STEPS")
print("-" * 62)
print("""
These results come from a generated portfolio dataset. They are not
verified Canadian population or health-system estimates.

Potential next steps for a real-world study:
1. Obtain and validate authoritative source data and definitions.
2. Recalculate differences, including denominators and uncertainty.
3. Work with clinical, community or operational partners to assess
   feasibility and avoid treating associations as causal effects.
4. Treat cost differences and savings as sensitivity-tested scenarios,
   not realized outcomes or established policy recommendations.
""")
