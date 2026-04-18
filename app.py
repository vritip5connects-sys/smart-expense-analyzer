import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ----------------------------
# TITLE
# ----------------------------
st.title("💰 Smart Expense Analyzer & Financial Health Predictor")
st.markdown("Analyze your spending, visualize trends, and predict future expenses.")

st.write("---")

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("data.csv")

# ----------------------------
# CATEGORIZATION
# ----------------------------
def categorize(desc):
    desc = desc.lower()
    
    if "swiggy" in desc or "zomato" in desc or "restaurant" in desc or "groceries" in desc:
        return "Food"
    elif "uber" in desc or "metro" in desc or "bus" in desc or "flight" in desc:
        return "Travel"
    elif "amazon" in desc or "shopping" in desc:
        return "Shopping"
    elif "bill" in desc or "netflix" in desc:
        return "Bills"
    else:
        return "Other"

df["Category"] = df["Description"].apply(categorize)

# ----------------------------
# SHOW DATA
# ----------------------------
st.subheader("📄 Categorized Expense Data")
st.write(df)

st.write("---")

# ----------------------------
# CATEGORY CHART
# ----------------------------
st.subheader("📊 Spending by Category")

category_sum = df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots()
category_sum.plot(kind="bar", ax=ax)

st.pyplot(fig)

st.write("---")

# ----------------------------
# MONTHLY TREND
# ----------------------------
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month

monthly = df.groupby("Month")["Amount"].sum()

st.subheader("📈 Monthly Spending Trend")

fig2, ax2 = plt.subplots()
monthly.plot(marker='o', ax=ax2)

st.pyplot(fig2)

st.write("---")

# ----------------------------
# ML PREDICTION
# ----------------------------
st.subheader("🔮 Next Month Prediction")

X = monthly.index.values.reshape(-1, 1)
y = monthly.values

model = LinearRegression()
model.fit(X, y)

next_month = [[monthly.index.max() + 1]]
prediction = model.predict(next_month)

predicted_value = abs(int(prediction[0]))

st.success(f"Predicted next month spending: ₹{predicted_value}")

st.write("---")

# ----------------------------
# FINANCIAL HEALTH SCORE
# ----------------------------
st.subheader("💡 Financial Health Score")

total_spent = abs(df["Amount"].sum())

if total_spent < 10000:
    score = "Good ✅"
elif total_spent < 25000:
    score = "Moderate ⚠️"
else:
    score = "Poor ❌"

st.info(f"Your financial health is: {score}")

st.write("---")

# ----------------------------
# KEY INSIGHT
# ----------------------------
st.subheader("📌 Key Insight")

top_category = category_sum.abs().idxmax()
st.write(f"You spend the most on: **{top_category}**")