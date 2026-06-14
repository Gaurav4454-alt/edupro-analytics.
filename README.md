# 🎓 EduPro — Instructor Performance & Course Quality Evaluation

> **A Data-Driven Analytics Framework for Online Education**  
> Dataset: 60 Instructors · 60 Courses · 10,000 Transactions · 3,000 Users

---

## 📌 Project Overview

This project builds a comprehensive evaluation framework for instructor performance and course quality on EduPro, an online learning platform. By integrating instructor profiles, course catalogs, and enrollment transactions, the analysis uncovers actionable insights that can directly improve teaching effectiveness and learner satisfaction.

---

## 🔍 Key Findings

| Finding | Insight |
|---------|---------|
| Experience → Teaching Quality | r = +0.598 — experience meaningfully improves instructor ratings |
| Instructor–Course Rating Correlation | r = −0.002 — course quality is independent of instructor credentials |
| Enrollment Concentration | 75% of enrollments captured by High-rated instructors (>3.5 rating) |
| Top Category | Marketing (Avg Course Rating: 3.69) |
| Weakest Category | Business (Avg Course Rating: 2.69) |
| Technical Expert Paradox | ML instructors rated 4.89, but their courses only 3.05 |

---

## 📊 KPIs

| KPI | Value |
|-----|-------|
| Average Teacher Rating | 3.12 / 5.0 |
| Average Course Rating | 3.10 / 5.0 |
| Rating Consistency Index | 0.95 (Std Dev) |
| Experience Impact Score | +0.598 (Pearson r) |
| Enrollment Influence Ratio | 75.0% |

---

## 🗂️ Project Structure

```
edupro-analytics/
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── EduPro_Online_Platform.xlsx     # Source dataset
├── EduPro_Analytics_Report.xlsx    # Full Excel analytics report
├── research_paper.md               # Research paper (EDA + Insights)
└── README.md
```

---

## 🚀 Run the Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

---

## 📁 Deliverables

- ✅ **Research Paper** — Full EDA, correlation analysis, recommendations
- ✅ **Streamlit Dashboard** — Interactive analytics with filters
- ✅ **Excel Analytics Report** — 7-sheet professional workbook with charts

---

## 🛠️ Tech Stack

- Python 3.11
- Streamlit 1.32+
- Plotly Express & Graph Objects
- pandas, numpy, scipy
- openpyxl (Excel generation)

---

## 📚 Dataset Fields Used

**Teachers:** TeacherID, TeacherName, Age, Gender, Expertise, YearsOfExperience, TeacherRating  
**Courses:** CourseID, CourseName, CourseCategory, CourseLevel, CourseRating  
**Transactions:** TransactionID, UserID, CourseID, TeacherID, TransactionDate, Amount

---

## 👤 Author

Submitted as part of EduPro Platform Analytics Project  
*May 2026*
