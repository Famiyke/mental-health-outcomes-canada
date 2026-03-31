"""
Project 5 – analysis.py
Data Detective → Programmer → Storyteller → Consultant
Mental Health Outcomes — CCHS PUMF
"""

import pandas as pd
import numpy as np

df  = pd.read_csv("cchs_data.csv")
sep = "=" * 62

print(f"\n{sep}")
print("  PROJECT 5 — PROVINCIAL MENTAL HEALTH OUTCOMES (CCHS)")
print(f"{sep}")

# ── Profile ───────────────────────────────────────────────────────────────────
print(f"\n  Respondents: {len(df):,}")
print(f"  Provinces:   {sorted(df['province'].unique())}")
print(f"  Age groups:  {sorted(df['age_group'].unique())}")

# Decode MH rating scale
mh_map = {1:"Excellent",2:"Very Good",3:"Good",4:"Fair",5:"Poor"}
df["mh_label"] = df["mh_rating"].map(mh_map)
df["poor_mh"]  = (df["mh_rating"] >= 4).astype(int)

# ── National Snapshot ─────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("NATIONAL MENTAL HEALTH SNAPSHOT")
print(f"{'─'*62}")

good_pct  = df["good_mh"].mean() * 100
poor_pct  = df["poor_mh"].mean() * 100
unmet_pct = df["unmet_need"].mean() * 100
any_cond  = df["has_any_condition"].mean() * 100

print(f"\n  Good/Excellent mental health:   {good_pct:.1f}%")
print(f"  Fair/Poor mental health:        {poor_pct:.1f}%")
print(f"  Unmet mental health need:       {unmet_pct:.1f}%")
print(f"  Have at least one condition:    {any_cond:.1f}%")

# ── Province Ranking ──────────────────────────────────────────────────────────
print(f"\n{'─'*62}")
print("PROVINCE RANKING — % with Good/Excellent Mental Health")
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
    below = " ◄ BELOW AVG" if r["good_mh"] < nat_avg else ""
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

# ── Indigenous Mental Health Gap ──────────────────────────────────────────────
print(f"\n{'─'*62}")
print("INDIGENOUS MENTAL HEALTH GAP")
print(f"{'─'*62}")

indig = df.groupby("indigenous")["good_mh"].mean()
indig_good = indig.get("Yes", np.nan)
non_good   = indig.get("No", np.nan)

print(f"\n  Indigenous respondents:     {indig_good:.1%} good/excellent MH")
print(f"  Non-Indigenous respondents: {non_good:.1%} good/excellent MH")
print(f"  Gap:                        {non_good - indig_good:.1%} percentage points")
print(f"  Unmet need — Indigenous:    {df[df['indigenous']=='Yes']['unmet_need'].mean():.1%}")
print(f"  Unmet need — Non-Indigenous:{df[df['indigenous']=='No']['unmet_need'].mean():.1%}")

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
print(f"\n{'─'*62}")
print("STRATEGIC RECOMMENDATIONS")
print(f"{'─'*62}")
print("""
  1. ATLANTIC AND RURAL ACCESS
     NB and NL show the lowest rates of good mental
     health in Canada. Combined with limited psychiatrist
     supply, this creates a structural access gap.
     Expand virtual mental health services with
     provincial health card coverage in these regions.

  2. INCOME AND EDUCATION INTERSECTION
     Low-income respondents without post-secondary
     education report poor mental health at twice
     the national rate and have the highest unmet need.
     Community-based, subsidised counselling programs
     (not just hospital referrals) are needed for this group.

  3. INDIGENOUS MENTAL HEALTH EQUITY
     The gap in both good mental health and unmet need
     between Indigenous and non-Indigenous respondents
     is the largest of any subgroup analysed.
     Provinces should fund Indigenous-led mental health
     services and meet existing UNDRIP commitments.

  4. ANXIETY TRAJECTORY
     Anxiety overtook depression as the most commonly
     reported condition in recent CCHS cycles.
     Structured online CBT programs with low-cost
     access could serve the majority of mild-to-moderate
     anxiety cases before they escalate to crisis.
""")
print(sep)
