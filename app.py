import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Smart Student Life System", layout="wide")

st.title("🎓 Smart Student Life System")

menu = st.sidebar.selectbox(
    "Choose Module",
    ["Study Planner", "Productivity Tracker", "Finance Planner"]
)

# ================= STUDY DATA =================
subjects = [
    ["Mathematics",5,5],["Physics",5,5],["Chemistry",4,4],
    ["Computer Science",3,5],["English",2,3],["Biology",4,3],
    ["Economics",3,4],["Statistics",4,5],["AI",5,5],
    ["Machine Learning",4,5]
]

df_sub = pd.DataFrame(subjects, columns=["subject","difficulty","priority"])

# ================= SESSION STORAGE =================
if "productivity" not in st.session_state:
    st.session_state.productivity = []

if "finance" not in st.session_state:
    st.session_state.finance = []

# ================= STUDY PLANNER =================
if menu == "Study Planner":

    st.header("📚 Study Planner")

    selected = st.multiselect(
        "Select Subjects",
        df_sub["subject"],
        default=df_sub["subject"].tolist()[:3]
    )

    hours = st.slider("Study Hours", 1, 12)

    if st.button("Generate Plan"):

        df = df_sub[df_sub["subject"].isin(selected)].copy()

        df["weight"] = df["difficulty"] * df["priority"]
        total = df["weight"].sum()

        df["allocated"] = (df["weight"] / total) * hours

        st.subheader("📅 Study Plan")

        for _, row in df.iterrows():
            st.write(f"{row['subject']} → {round(row['allocated'],2)} hrs")

        # timetable
        st.subheader("📆 Timetable")
        time = 9
        for _, row in df.iterrows():
            for _ in range(int(round(row["allocated"]))):
                st.write(f"{time}:00 - {time+1}:00 → {row['subject']}")
                time += 1

        # chart
        fig, ax = plt.subplots()
        ax.pie(df["allocated"], labels=df["subject"], autopct='%1.1f%%')
        st.pyplot(fig)

# ================= PRODUCTIVITY =================
elif menu == "Productivity Tracker":

    st.header("📊 Productivity Tracker")

    study = st.number_input("Study Hours", 0, 24)
    sleep = st.number_input("Sleep Hours", 0, 24)
    focus = st.slider("Focus Score", 0, 100)

    if st.button("Add Data"):
        st.session_state.productivity.append([study, sleep, focus])

    if st.session_state.productivity:

        df = pd.DataFrame(st.session_state.productivity,
                          columns=["study","sleep","focus"])

        st.dataframe(df)

        # graph
        fig, ax = plt.subplots()
        ax.plot(df["focus"], marker='o')
        st.pyplot(fig)

        # average
        avg = df["focus"].mean()
        st.write("Average Focus:", round(avg,2))

        # prediction
        if len(df) > 1:
            x = np.arange(len(df))
            y = df["focus"]

            m, c = np.polyfit(x, y, 1)

            future = m*(len(df)) + c
            st.write("Predicted Next Focus:", round(future,2))

        # insight
        if avg < 60:
            st.warning("Low productivity")
        else:
            st.success("Good productivity")

# ================= FINANCE =================
elif menu == "Finance Planner":

    st.header("💰 Finance Planner")

    category = st.selectbox(
        "Category",
        ["Food","Transport","Shopping","Entertainment","Other"]
    )

    income = st.number_input("Income", 0)
    expense = st.number_input("Expense", 0)

    if st.button("Add Transaction"):
        st.session_state.finance.append([category, income, expense])

    if st.session_state.finance:

        df = pd.DataFrame(st.session_state.finance,
                          columns=["category","income","expense"])

        st.dataframe(df)

        total_income = df["income"].sum()
        total_expense = df["expense"].sum()

        st.write("Total Income:", total_income)
        st.write("Total Expense:", total_expense)
        st.write("Savings:", total_income - total_expense)

        # pie chart
        cat = df.groupby("category")["expense"].sum()

        fig, ax = plt.subplots()
        ax.pie(cat, labels=cat.index, autopct='%1.1f%%')
        st.pyplot(fig)

        # insight
        if total_expense > total_income:
            st.error("Overspending")
        else:
            st.success("Good financial management")