"""Regression checks for the generated mental-health demonstration data.

Run after `python simulate_cchs.py`. This is a technical data-quality check,
not a validation against Statistics Canada survey records.
"""
import pandas as pd

df = pd.read_csv("cchs_data.csv")
required = {"respondent_id", "province", "mh_rating", "good_mh", "unmet_need",
            "indigenous", "income_group"}
missing = required - set(df.columns)
assert not missing, f"Missing expected columns: {missing}"
assert len(df) == 5000, f"Expected 5,000 synthetic rows, found {len(df)}"
assert df["respondent_id"].is_unique, "Respondent IDs must be unique"
assert df["mh_rating"].between(1, 5).all(), "Invalid five-level self-rated MH values"
assert df["good_mh"].isin([0, 1]).all(), "Unexpected good_mh coding"
expected_good = df["mh_rating"].isin([1,2,3]).astype(int)
assert df["good_mh"].equals(expected_good), "Good MH flag must match 1-3 ratings"
fair_poor = df["mh_rating"].isin([4,5]).astype(int)
assert ((expected_good + fair_poor) == 1).all(), "Rating groups not exhaustive"
assert abs(100*(expected_good.mean() + fair_poor.mean()) - 100) < 1e-9
assert df["unmet_need"].isin([0,1]).all()
n_by_province = df.groupby("province").size()
small = n_by_province[n_by_province < 30]
print("PASS: synthetic survey category coding and denominator checks")
print("Subgroups below 30 synthetic observations (suppress in presented comparison):")
print(small.to_string() if len(small) else "none")
print("Synthetic data remain nonrepresentative and unweighted.")
