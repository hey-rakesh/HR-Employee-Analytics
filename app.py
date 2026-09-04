import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="HR Employee Analytics Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------





BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "emp_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


df = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏠 HR Employee Analytics Dashboard")

st.markdown(
    "Analyze employee workforce, salary, attrition, and performance data."
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔍 Filters")


department = st.sidebar.multiselect(
    "Select Department",
    options=df["department"].dropna().unique(),
    default=df["department"].dropna().unique()
)


gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["gender"].dropna().unique(),
    default=df["gender"].dropna().unique()
)


attrition = st.sidebar.multiselect(
    "Select Attrition Status",
    options=df["attrition_status"].dropna().unique(),
    default=df["attrition_status"].dropna().unique()
)


# APPLY FILTERS

filtered_df = df[
    (df["department"].isin(department)) &
    (df["gender"].isin(gender)) &
    (df["attrition_status"].isin(attrition))
]


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

st.header("📊 Overview")


total_employees = filtered_df["employee_id"].nunique()

average_salary = filtered_df["salary"].mean()

average_age = filtered_df["age"].mean()

attrition_rate = (
    filtered_df["attrition_status"]
    .eq("Yes")
    .mean() * 100
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Employees",
    f"{total_employees:,}"
)


col2.metric(
    "Average Salary",
    f"₹{average_salary:,.0f}"
)


col3.metric(
    "Average Age",
    f"{average_age:.1f} Years"
)


col4.metric(
    "Attrition Rate",
    f"{attrition_rate:.2f}%"
)


st.divider()


# ==================================================
# WORKFORCE ANALYSIS
# ==================================================

st.header("👥 Workforce Analysis")


col1, col2 = st.columns(2)


# --------------------------------
# EMPLOYEES BY DEPARTMENT
# --------------------------------

with col1:

    st.subheader("Employees by Department")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.countplot(
        data=filtered_df,
        x="department",
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)


# --------------------------------
# GENDER DISTRIBUTION
# --------------------------------

with col2:

    st.subheader("Gender Distribution")

    gender_count = filtered_df["gender"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.pie(
        gender_count.values,
        labels=gender_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)


# --------------------------------
# AGE DISTRIBUTION
# --------------------------------

st.subheader("Age Distribution")

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    data=filtered_df,
    x="age",
    bins=10,
    kde=True,
    ax=ax
)

st.pyplot(fig)


st.divider()


# ==================================================
# SALARY ANALYSIS
# ==================================================

st.header("💰 Salary Analysis")


col1, col2 = st.columns(2)


# --------------------------------
# AVERAGE SALARY BY DEPARTMENT
# --------------------------------

with col1:

    st.subheader("Average Salary by Department")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=filtered_df,
        x="department",
        y="salary",
        estimator="mean",
        errorbar=None,
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)


# --------------------------------
# SALARY DISTRIBUTION
# --------------------------------

with col2:

    st.subheader("Salary Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        data=filtered_df,
        x="salary",
        bins=15,
        kde=True,
        ax=ax
    )

    st.pyplot(fig)


# --------------------------------
# EXPERIENCE VS SALARY
# --------------------------------

st.subheader("Experience vs Salary")

fig, ax = plt.subplots(figsize=(10, 6))

sns.scatterplot(
    data=filtered_df,
    x="experience_years",
    y="salary",
    hue="department",
    ax=ax
)

st.pyplot(fig)


st.divider()


# ==================================================
# ATTRITION ANALYSIS
# ==================================================

st.header("🚪 Attrition Analysis")


col1, col2 = st.columns(2)


# --------------------------------
# OVERALL ATTRITION
# --------------------------------

with col1:

    st.subheader("Overall Attrition")

    attrition_count = (
        filtered_df["attrition_status"]
        .value_counts()
    )

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.pie(
        attrition_count.values,
        labels=attrition_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    st.pyplot(fig)


# --------------------------------
# ATTRITION BY DEPARTMENT
# --------------------------------

with col2:

    st.subheader("Attrition by Department")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.countplot(
        data=filtered_df,
        x="department",
        hue="attrition_status",
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)


# --------------------------------
# ATTRITION BY JOB ROLE
# --------------------------------

st.subheader("Attrition by Job Role")

fig, ax = plt.subplots(figsize=(12, 6))

sns.countplot(
    data=filtered_df,
    x="job_role",
    hue="attrition_status",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)


st.divider()


# ==================================================
# CORRELATION ANALYSIS
# ==================================================

st.header("🔗 Correlation Analysis")


numeric_df = filtered_df.select_dtypes(
    include="number"
)


correlation = numeric_df.corr()


fig, ax = plt.subplots(figsize=(12, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax
)


st.pyplot(fig)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "HR Employee Analytics Dashboard | Built with Python, Pandas, Seaborn and Streamlit"
)
