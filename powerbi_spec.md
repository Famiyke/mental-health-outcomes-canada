# Power BI Dashboard Spec
## Mental Health Outcomes — Canada (CCHS)

**File:** `mental_health_outcomes.pbix`
**Data connection:** `cchs_data.csv` — 5,000 respondents, 17 columns
**Load via:** Get Data → Text/CSV → select cchs_data.csv

**Column types to set after loading:**
- `respondent_id`, `mh_rating`, `good_mh`, `unmet_need`, `saw_mh_provider` → Whole Number
- `Depression`, `Anxiety`, `PTSD`, `Bipolar`, `Substance_Use`, `has_any_condition` → Whole Number
- `province`, `age_group`, `sex`, `income_group`, `education`, `indigenous` → Text

---

## DAX Measures

Create these measures in a dedicated `_Measures` table:

```dax
Good MH % =
ROUND(AVERAGE(cchs[good_mh]) * 100, 1)

Poor MH % =
ROUND(
    COUNTROWS(FILTER(cchs, cchs[mh_rating] >= 4))
    / COUNTROWS(cchs) * 100
, 1)

Unmet Need % =
ROUND(AVERAGE(cchs[unmet_need]) * 100, 1)

Anxiety Prevalence % =
ROUND(AVERAGE(cchs[Anxiety]) * 100, 1)

Depression Prevalence % =
ROUND(AVERAGE(cchs[Depression]) * 100, 1)

Indigenous Unmet Ratio =
VAR indig_unmet =
    CALCULATE(AVERAGE(cchs[unmet_need]),
              cchs[indigenous] = "Yes")
VAR non_unmet =
    CALCULATE(AVERAGE(cchs[unmet_need]),
              cchs[indigenous] = "No")
RETURN
DIVIDE(indig_unmet, non_unmet)

Low Income Good MH % =
CALCULATE(
    AVERAGE(cchs[good_mh]) * 100,
    cchs[income_group] = "< $30K"
)

High Income Good MH % =
CALCULATE(
    AVERAGE(cchs[good_mh]) * 100,
    cchs[income_group] = "$100K+"
)

Income MH Gap =
[High Income Good MH %] - [Low Income Good MH %]
```

---

## Page 1 — National Snapshot

**Visual 1 — KPI cards (4 cards in a row)**
- Good MH %: `[Good MH %]` — green
- Poor MH %: `[Poor MH %]` — red
- Unmet Need %: `[Unmet Need %]` — amber
- Any Condition %: `ROUND(AVERAGE(cchs[has_any_condition])*100,1)` — neutral

**Visual 2 — Horizontal bar chart: Condition prevalence**
- Y-axis: Condition labels (use a separate table or UNION measure)
- X-axis: Prevalence %
- Sort descending by prevalence
- Highlight Anxiety bar in red to show it exceeds Depression
- Title: "Mental Health Condition Prevalence — National"

**Visual 3 — Donut: Good vs Poor MH**
- Values: `[Good MH %]`, `[Poor MH %]`
- Green and red segments
- Title: "National Mental Health Distribution"

**Page slicer:** Year (if multi-year data loaded)

---

## Page 2 — Provincial Analysis

**Visual 1 — Filled Map**
- Location: `province` (mark as Province/State → Canada)
- Color saturation: `[Good MH %]`
- Color scale: red (low) → green (high)
- Tooltip: Province, Good MH %, Unmet Need %

**Visual 2 — Bar chart: Province ranking**
- Y-axis: `province`
- X-axis: `[Good MH %]`
- Sort ascending (worst at top)
- Add constant line at national average
- Title: "Provincial Good Mental Health Ranking"

**Visual 3 — Table: Province scorecard**
Columns: Province, Good MH %, Poor MH %, Unmet Need %, n
Conditional formatting on Good MH %: red → green scale

**DAX — Atlantic Flag:**
```dax
Atlantic Flag =
IF(
    SELECTEDVALUE(cchs[province]) IN {"NB","NL","NS","PE"},
    "Atlantic",
    "Other"
)
```

---

## Page 3 — Demographic Breakdown

**Visual 1 — Clustered bar: Income gradient**
- Y-axis: `income_group`
- X-axis: `[Good MH %]`
- Sort by income ascending (< $30K at bottom)
- Title: "Good Mental Health by Income Group"
- Add data labels showing exact %

**Visual 2 — Clustered bar: Age group**
- Y-axis: `age_group`
- X-axis: `[Good MH %]`
- Title: "Good Mental Health by Age Group"

**Visual 3 — Card: Income gap**
- Measure: `[Income MH Gap]`
- Label: "Good MH Gap: Lowest vs Highest Income"
- Format: 0.0 "pp"

**DAX — High Risk Flag:**
```dax
High Risk Group =
IF(
    cchs[income_group] = "< $30K"
    && cchs[education] IN {"Less than HS","High School"},
    "High Risk",
    "Other"
)
```

---

## Page 4 — Equity Analysis

**Visual 1 — Clustered bar: Indigenous vs non-Indigenous**
- Values: Good MH %, Unmet Need %
- Legend: `indigenous`
- Title: "Indigenous vs Non-Indigenous Mental Health"

**Visual 2 — KPI card: Indigenous unmet need ratio**
- Measure: `[Indigenous Unmet Ratio]`
- Label: "Indigenous Unmet Need Ratio vs Non-Indigenous"
- Format: 0.0 "x"

**Visual 3 — Matrix: Province × Income**
- Rows: `province`
- Columns: `income_group`
- Values: `[Good MH %]`
- Conditional formatting: red → green
- Title: "Good MH % by Province and Income Group"

---

## Theme and Colours

| Element | Hex |
|---------|-----|
| Good MH / positive | `#27AE60` |
| Poor MH / negative | `#E74C3C` |
| Unmet need / warning | `#F39C12` |
| Indigenous focus | `#2980B9` |
| Background | `#FAFAFA` |
| Card background | `#FFFFFF` |
| Grid lines | `#E8E8E8` |
