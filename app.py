import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="EduPro Analytics", layout="wide", page_icon="🎓")

@st.cache_data
def load_data():
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    xl = pd.read_excel(os.path.join(base, "EduPro_Online_Platform.xlsx"), sheet_name=None)
    teachers = xl["Teachers"]
    courses = xl["Courses"]
    transactions = xl["Transactions"]
    merged = transactions.merge(teachers, on="TeacherID").merge(courses, on="CourseID")
    merged["TeacherTier"] = pd.cut(
        merged["TeacherRating"], bins=[0, 2.5, 3.5, 5], labels=["Low", "Mid", "High"]
    )
    return teachers, courses, transactions, merged

teachers, courses, transactions, merged = load_data()

# --- Sidebar Filters ---
st.sidebar.image("https://img.icons8.com/color/96/graduation-cap.png", width=60)
st.sidebar.title("🎓 EduPro Filters")

expertise_options = ["All"] + sorted(teachers["Expertise"].unique().tolist())
selected_expertise = st.sidebar.multiselect("Instructor Expertise", expertise_options, default=["All"])

category_options = ["All"] + sorted(courses["CourseCategory"].unique().tolist())
selected_category = st.sidebar.multiselect("Course Category", category_options, default=["All"])

level_options = ["All"] + sorted(courses["CourseLevel"].unique().tolist())
selected_level = st.sidebar.multiselect("Course Level", level_options, default=["All"])

rating_range = st.sidebar.slider("Teacher Rating Range", 1.0, 5.0, (1.0, 5.0), 0.1)

# --- Apply Filters ---
filtered = merged.copy()
if "All" not in selected_expertise and selected_expertise:
    filtered = filtered[filtered["Expertise"].isin(selected_expertise)]
if "All" not in selected_category and selected_category:
    filtered = filtered[filtered["CourseCategory"].isin(selected_category)]
if "All" not in selected_level and selected_level:
    filtered = filtered[filtered["CourseLevel"].isin(selected_level)]
filtered = filtered[
    (filtered["TeacherRating"] >= rating_range[0])
    & (filtered["TeacherRating"] <= rating_range[1])
]

# --- KPI Cards ---
st.title("🎓 EduPro — Instructor & Course Quality Dashboard")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
avg_tr = filtered["TeacherRating"].mean()
avg_cr = filtered["CourseRating"].mean()
rci = teachers["TeacherRating"].std()
eis = teachers[["YearsOfExperience", "TeacherRating"]].corr().iloc[0, 1]
total_enroll = len(filtered)

col1.metric("📊 Avg Teacher Rating", f"{avg_tr:.2f}" if not np.isnan(avg_tr) else "N/A", "/ 5.0")
col2.metric("📚 Avg Course Rating", f"{avg_cr:.2f}" if not np.isnan(avg_cr) else "N/A", "/ 5.0")
col3.metric("📈 Rating Consistency Index", f"{rci:.2f}", "Lower = more consistent")
col4.metric("🎯 Experience Impact Score", f"{eis:.3f}", "Correlation")
col5.metric("🧑‍🎓 Filtered Enrollments", f"{total_enroll:,}")

st.markdown("---")

# --- Row 1: Instructor Leaderboard + Rating Distribution ---
col_a, col_b = st.columns([1.2, 1])

with col_a:
    st.subheader("🏆 Instructor Performance Leaderboard")
    leaderboard = (
        filtered.groupby(["TeacherName", "Expertise", "YearsOfExperience"])
        .agg(TeacherRating=("TeacherRating", "mean"), Enrollments=("TransactionID", "count"), AvgCourseRating=("CourseRating", "mean"))
        .reset_index()
        .sort_values("TeacherRating", ascending=False)
        .head(15)
        .round(2)
    )
    leaderboard.index = range(1, len(leaderboard) + 1)
    st.dataframe(
        leaderboard.rename(columns={"TeacherName": "Instructor", "YearsOfExperience": "Exp (yrs)", "AvgCourseRating": "Avg Course Rating"}),
        use_container_width=True,
        height=360,
    )

with col_b:
    st.subheader("📊 Teacher Rating Distribution")
    fig_hist = px.histogram(
        teachers[teachers["TeacherRating"].between(rating_range[0], rating_range[1])],
        x="TeacherRating",
        nbins=20,
        color_discrete_sequence=["#4F8EF7"],
        labels={"TeacherRating": "Teacher Rating"},
    )
    fig_hist.update_layout(height=360, margin=dict(t=20, b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Row 2: Experience vs Ratings ---
st.subheader("🔍 Experience vs Performance Analysis")
col_c, col_d = st.columns(2)

with col_c:
    t_data = filtered.drop_duplicates("TeacherID")
    fig_scatter1 = px.scatter(
        t_data, x="YearsOfExperience", y="TeacherRating",
        color="Expertise", size_max=12,
        trendline="ols",
        hover_data=["TeacherName"],
        labels={"YearsOfExperience": "Years of Experience", "TeacherRating": "Teacher Rating"},
        title="Experience vs Teacher Rating",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_scatter1.update_layout(height=380, margin=dict(t=40))
    st.plotly_chart(fig_scatter1, use_container_width=True)

with col_d:
    fig_scatter2 = px.scatter(
        filtered, x="YearsOfExperience", y="CourseRating",
        color="CourseLevel", trendline="ols",
        hover_data=["CourseName"],
        labels={"YearsOfExperience": "Years of Experience", "CourseRating": "Course Rating"},
        title="Experience vs Course Rating",
        color_discrete_sequence=["#F7C948", "#4F8EF7", "#E85D75"],
    )
    fig_scatter2.update_layout(height=380, margin=dict(t=40))
    st.plotly_chart(fig_scatter2, use_container_width=True)

# --- Row 3: Category Heatmap + Tier Analysis ---
col_e, col_f = st.columns(2)

with col_e:
    st.subheader("🗺️ Course Quality Heatmap by Category & Level")
    heatmap_data = (
        filtered.groupby(["CourseCategory", "CourseLevel"])["CourseRating"]
        .mean()
        .reset_index()
        .pivot(index="CourseCategory", columns="CourseLevel", values="CourseRating")
        .round(2)
    )
    if not heatmap_data.empty:
        fig_heat = px.imshow(
            heatmap_data,
            color_continuous_scale="RdYlGn",
            zmin=1, zmax=5,
            text_auto=True,
            labels=dict(color="Avg Rating"),
            aspect="auto",
        )
        fig_heat.update_layout(height=420, margin=dict(t=20))
        st.plotly_chart(fig_heat, use_container_width=True)

with col_f:
    st.subheader("📦 Enrollments by Instructor Rating Tier")
    tier_data = (
        filtered.groupby("TeacherTier", observed=True)
        .agg(Enrollments=("TransactionID", "count"), AvgCourseRating=("CourseRating", "mean"))
        .reset_index()
    )
    fig_tier = make_subplots(specs=[[{"secondary_y": True}]])
    fig_tier.add_trace(
        go.Bar(x=tier_data["TeacherTier"], y=tier_data["Enrollments"], name="Enrollments", marker_color=["#E85D75", "#F7C948", "#4BCB8A"]),
        secondary_y=False,
    )
    fig_tier.add_trace(
        go.Scatter(x=tier_data["TeacherTier"], y=tier_data["AvgCourseRating"].round(2), name="Avg Course Rating", mode="lines+markers", marker=dict(size=10, color="#4F8EF7"), line=dict(width=3)),
        secondary_y=True,
    )
    fig_tier.update_yaxes(title_text="Enrollments", secondary_y=False)
    fig_tier.update_yaxes(title_text="Avg Course Rating", secondary_y=True)
    fig_tier.update_layout(height=420, margin=dict(t=20), legend=dict(orientation="h"))
    st.plotly_chart(fig_tier, use_container_width=True)

# --- Row 4: Expertise Performance ---
st.subheader("🧠 Expertise-Wise Performance Comparison")
col_g, col_h = st.columns(2)

with col_g:
    exp_perf = (
        filtered.groupby("Expertise")
        .agg(AvgTeacherRating=("TeacherRating", "mean"), AvgCourseRating=("CourseRating", "mean"), Instructors=("TeacherID", "nunique"))
        .reset_index()
        .sort_values("AvgTeacherRating", ascending=True)
        .round(2)
    )
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(y=exp_perf["Expertise"], x=exp_perf["AvgTeacherRating"], name="Avg Teacher Rating", orientation="h", marker_color="#4F8EF7"))
    fig_bar.add_trace(go.Bar(y=exp_perf["Expertise"], x=exp_perf["AvgCourseRating"], name="Avg Course Rating", orientation="h", marker_color="#F7C948"))
    fig_bar.update_layout(barmode="group", height=420, margin=dict(t=20), legend=dict(orientation="h"))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_h:
    st.subheader("🚻 Gender Distribution & Ratings")
    gender_data = (
        filtered.drop_duplicates("TeacherID")
        .groupby(["Gender_x", "Expertise"])["TeacherRating"]
        .mean()
        .reset_index()
        .rename(columns={"Gender_x": "Gender"})
    )
    fig_gender = px.box(
        filtered.drop_duplicates("TeacherID"),
        x="Expertise", y="TeacherRating", color="Gender_x",
        labels={"Gender_x": "Gender", "TeacherRating": "Teacher Rating"},
        color_discrete_sequence=["#4F8EF7", "#E85D75"],
    )
    fig_gender.update_layout(height=420, margin=dict(t=20), xaxis_tickangle=-30)
    st.plotly_chart(fig_gender, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("EduPro Analytics Dashboard | Instructor & Course Quality Evaluation | Built with Streamlit & Plotly")
