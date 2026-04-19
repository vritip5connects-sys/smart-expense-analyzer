import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Smart Expense Analyzer")
st.write("Analyze your spending and get insights")

st.write("----------------------------------------")

# Upload file
file = st.file_uploader("Upload your expense CSV", type=["csv"])

if file is not None:

    df = pd.read_csv(file)

    st.subheader("Raw Data")
    st.write(df)

    st.write("----------------------------------------")

    # Ensure correct format
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'])

    df['Month'] = df['Date'].dt.month_name()

    # 🔹 Category Analysis
    st.subheader("📊 Spending by Category")

    category_data = df.groupby('Category')['Amount'].sum()

    fig1, ax1 = plt.subplots()
    category_data.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    st.write("----------------------------------------")

    # 🔹 Monthly Trend
    st.subheader("📈 Monthly Spending Trend")

    monthly_data = df.groupby('Month')['Amount'].sum()

    fig2, ax2 = plt.subplots()
    monthly_data.plot(kind='line', marker='o', ax=ax2)
    st.pyplot(fig2)

    st.write("----------------------------------------")

    # 🔹 Insights
    st.subheader("🧠 Insights")

    total_spent = df['Amount'].sum()
    top_category = category_data.idxmax()

    st.write(f"Total Spending: ₹{int(total_spent):,}")
    st.write(f"Top Spending Category: {top_category}")

    # 🔹 Financial Health Score
    st.subheader("💡 Financial Health Score")

    income = st.number_input("Enter your monthly income", value=50000)

    if income > 0:
        savings = income - total_spent

        if savings > income * 0.3:
            st.success("Good financial health 👍")
        elif savings > 0:
            st.warning("Average financial health ⚠️")
        else:
            st.error("You are overspending 🚨")