"""THE APPPPPPP"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).parent
DATA = ROOT / "vancouver_food_businesses_sample.csv"

SEED = 461
CONTACTS_PER_WEEK = 10
NARROW_STATUSES = ["Cancelled", "Gone Out of Business"]
WIDE_STATUSES = NARROW_STATUSES + ["Pending", "Inactive"]
MIN_TYPE_N, MIN_AREA_N = 5, 8

CAT_FEATURES = ["businesstype_grouped", "localarea_grouped"]
NUM_FEATURES = ["numberofemployees"]
FEATURES = CAT_FEATURES + NUM_FEATURES
DELIVERABLE_COLUMNS = [
    "rank", "contact_week", "risk_band", "licencenumber", "businessname",
    "businesstype", "localarea", "numberofemployees", "risk_score",
]

st.set_page_config(page_title="Food business contact list", page_icon="🍽️",
                   layout="wide")


@st.cache_data
def load_prepared():
    frame = pd.read_csv(DATA)
    frame["failed_wide"] = frame["status"].isin(WIDE_STATUSES).astype(int)
    frame = (frame.sort_values("issueddate")
                  .drop_duplicates("licencenumber", keep="last")
                  .reset_index(drop=True))

    type_counts = frame["businesstype"].value_counts()
    rare_types = type_counts[type_counts < MIN_TYPE_N].index
    frame["businesstype_grouped"] = frame["businesstype"].where(
        ~frame["businesstype"].isin(rare_types), "Other")

    area_counts = frame["localarea"].value_counts()
    kept_areas = area_counts[area_counts >= MIN_AREA_N].index
    frame["localarea_grouped"] = frame["localarea"].where(
        frame["localarea"].isin(kept_areas), "Other areas")
    return frame, sorted(kept_areas)


@st.cache_resource
def fit_model(frame):
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES),
        ("num", "passthrough", NUM_FEATURES),
    ])
    pipeline = Pipeline([
        ("pre", preprocessor),
        ("clf", RandomForestClassifier(
            n_estimators=500, min_samples_leaf=3,
            class_weight="balanced_subsample", random_state=SEED, n_jobs=-1)),
    ])
    return pipeline.fit(frame[FEATURES], frame["failed_wide"])


def build_contact_list(frame, fitted_model):
    open_businesses = frame[frame["status"] == "Issued"].copy()
    open_businesses["risk_score"] = fitted_model.predict_proba(
        open_businesses[FEATURES])[:, 1]
    ranked = open_businesses.sort_values("risk_score", ascending=False).copy()
    ranked["rank"] = np.arange(1, len(ranked) + 1)
    ranked["contact_week"] = np.ceil(
        ranked["rank"] / CONTACTS_PER_WEEK).astype(int)
    ranked["risk_band"] = np.where(
        ranked["rank"] <= 30, "high",
        np.where(ranked["rank"] <= 70, "medium", "low"))
    return ranked


model_df, kept_areas = load_prepared()
model = fit_model(model_df)
contact_list = build_contact_list(model_df, model)
base_rate = model_df["failed_wide"].mean()

st.title("Food business contact list")
st.caption("Greater Vancouver Food Bank | IAT 461 final project | "
           "Mahdi Taziki (301373483)")

st.info(
    "This is a trial contact list for the 168 businesses with an Issued licence. "
    "The model ranks them using business type, neighbourhood, and employee count. "
    "It has not been tested on which open businesses close later, so a high rank "
    "does not mean that a business is expected to close.",
    icon="ℹ️")

st.sidebar.header("Filters")
bands = st.sidebar.multiselect(
    "Risk band", ["high", "medium", "low"], default=["high"])

max_week = int(contact_list["contact_week"].max())
week_range = st.sidebar.slider(
    "Contact week", min_value=1, max_value=max_week, value=(1, 3))

types = st.sidebar.multiselect(
    "Business type", sorted(contact_list["businesstype"].unique()), default=[])
areas = st.sidebar.multiselect(
    "Neighbourhood", sorted(contact_list["localarea"].dropna().unique()), default=[])

filtered = contact_list[
    contact_list["risk_band"].isin(bands)
    & contact_list["contact_week"].between(*week_range)]
if types:
    filtered = filtered[filtered["businesstype"].isin(types)]
if areas:
    filtered = filtered[filtered["localarea"].isin(areas)]

st.sidebar.markdown("---")
st.sidebar.caption(
    f"Model: random forest. Training records: {len(model_df)}. "
    f"Records in the failure group: {int(model_df['failed_wide'].sum())}. "
    f"Random seed: {SEED}.")

list_tab, check_tab, quality_tab = st.tabs(
    ["Contact list", "Try a business", "About the results"])

with list_tab:
    left, middle, right = st.columns(3)
    left.metric("Businesses shown", len(filtered))
    middle.metric("Issued businesses in total", len(contact_list))
    right.metric("Contact weeks shown", f"{week_range[0]} to {week_range[1]}")

    display = (filtered[DELIVERABLE_COLUMNS]
               .rename(columns={
                   "businessname": "business",
                   "businesstype": "type",
                   "localarea": "neighbourhood",
                   "numberofemployees": "employees",
               })
               .round({"risk_score": 3}))

    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button(
        "Download this view as CSV",
        display.to_csv(index=False).encode("utf-8"),
        file_name="contact_list_filtered.csv",
        mime="text/csv")

    st.markdown("#### Businesses shown by neighbourhood")
    by_area = (filtered.groupby("localarea").size()
               .sort_values(ascending=False).rename("businesses"))
    if len(by_area):
        st.bar_chart(by_area, color="#9A6FB0")
    else:
        st.caption("No businesses match the current filters.")

with check_tab:
    st.write(
        "Choose a business type, neighbourhood, and employee count. The app will "
        "show where that example would appear in the current list. The score is not "
        "a probability of closing.")

    col_a, col_b, col_c = st.columns(3)
    chosen_type = col_a.selectbox(
        "Business type", sorted(model_df["businesstype_grouped"].unique()))
    chosen_area = col_b.selectbox("Neighbourhood", kept_areas + ["Other areas"])
    employees = col_c.number_input(
        "Number of employees", min_value=0, max_value=2000, value=5, step=1)

    query = pd.DataFrame([{
        "businesstype_grouped": chosen_type,
        "localarea_grouped": chosen_area,
        "numberofemployees": float(employees),
    }])
    score = float(model.predict_proba(query)[:, 1][0])
    position = int((contact_list["risk_score"] > score).sum()) + 1
    week = int(np.ceil(position / CONTACTS_PER_WEEK))
    band = "high" if position <= 30 else "medium" if position <= 70 else "low"

    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Model score", f"{score:.3f}")
    metric_b.metric("Place in the list", f"{position} of {len(contact_list) + 1}")
    metric_c.metric("Band", band)

    st.write(
        f"This example would appear in contact week {week} if the list is followed "
        f"in order. Its score is {score:.3f}, but that does not mean a {score:.0%} "
        "chance of closing.")

    similar = contact_list[
        (contact_list["businesstype_grouped"] == chosen_type)
        & (contact_list["localarea_grouped"] == chosen_area)]
    if len(similar):
        st.write(
            f"The current list contains {len(similar)} issued businesses of this "
            f"type in this area, at positions {similar['rank'].min()} to "
            f"{similar['rank'].max()}.")

with quality_tab:
    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Cross-validated AP", "0.385",
                    f"{0.385 / base_rate:.2f} x random baseline")
    metric_b.metric("Cross-validated precision@10", "0.292",
                    f"base rate {base_rate:.3f}")
    metric_c.metric("Records in evaluation", len(model_df))

    st.markdown("#### How I tested the model")
    st.write(
        "I used 5-fold cross-validation repeated 10 times for the AP score. I also "
        "rebuilt the ranking 25 times with different splits to see how much the top "
        "positions changed. These tests used all 219 records. They did not follow "
        "the 168 Issued businesses to see what happened later.")

    st.markdown("#### Main result")
    st.write(
        "The random forest scored above the random baseline with all four failure "
        "labels I tested. Business type had the highest average importance, but the "
        "importance values changed across the validation folds.")

    st.markdown("#### Limits")
    st.write(
        "The score is not a probability. The list has not been tested on future "
        "closures, and the 168 Issued businesses were part of the training data. The "
        "model only knows the business type, neighbourhood, and employee count.")

    st.markdown("#### Data I would want next")
    st.write(
        "Licence records from several years would show which businesses were open in "
        "one year and closed later. I could then test the model on a later year instead "
        "of only using one snapshot.")

    st.markdown("#### Business types in the top 30")
    top = (contact_list.head(30).groupby("businesstype").size()
           .sort_values(ascending=False).rename("businesses"))
    st.bar_chart(top, color="#E45756")

    st.caption("See notebooks/03_Final_Model.ipynb for the full method and figures.")
