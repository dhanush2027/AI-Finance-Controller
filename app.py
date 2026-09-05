import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AI Finance Controller",
    page_icon="💰",
    layout="wide"
)

st.title("💰 AI Finance Controller")
st.caption("AI-powered financial analysis and spending insights")

# Demo transaction data
demo = pd.DataFrame({
    "Date": pd.to_datetime([
        "2026-08-01", "2026-08-02", "2026-08-03",
        "2026-08-04", "2026-08-05", "2026-08-06",
        "2026-08-07", "2026-08-08", "2026-08-09",
        "2026-08-10"
    ]),
    "Description": [
        "Salary Credit", "Rent", "Grocery Store",
        "Uber", "Restaurant", "Electricity Bill",
        "Online Shopping", "Fuel", "Subscription",
        "Pharmacy"
    ],
    "Category": [
        "Income", "Housing", "Food", "Transport",
        "Food", "Utilities", "Shopping", "Transport",
        "Subscription", "Health"
    ],
    "Amount": [
        50000, 15000, 4200, 850, 1800,
        2200, 3500, 2500, 799, 1200
    ],
    "Type": [
        "Income", "Expense", "Expense", "Expense",
        "Expense", "Expense", "Expense", "Expense",
        "Expense", "Expense"
    ]
})

uploaded = st.file_uploader(
    "Upload your transaction CSV",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)
    st.success("Transaction file loaded successfully.")
else:
    df = demo.copy()
    st.info("Demo transactions are currently displayed.")

required_columns = {"Category", "Amount", "Type"}

if not required_columns.issubset(df.columns):
    st.error(
        "CSV must contain Category, Amount and Type columns."
    )
    st.stop()

df["Amount"] = pd.to_numeric(
    df["Amount"], errors="coerce"
).fillna(0)

df["Type"] = df["Type"].astype(str).str.title()

# Financial calculations
income = df.loc[
    df["Type"] == "Income", "Amount"
].sum()

expenses = df.loc[
    df["Type"] == "Expense", "Amount"
].sum()

balance = income - expenses

savings_rate = (
    balance / income * 100
    if income > 0 else 0
)

# Dashboard
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💵 Total Income",
    f"₹{income:,.0f}"
)

col2.metric(
    "💳 Total Expenses",
    f"₹{expenses:,.0f}"
)

col3.metric(
    "💰 Balance",
    f"₹{balance:,.0f}"
)

col4.metric(
    "📈 Savings Rate",
    f"{savings_rate:.1f}%"
)

st.divider()

# Spending analysis
st.subheader("📊 Spending by Category")

expense_df = df[
    df["Type"] == "Expense"
]

category = (
    expense_df
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category)

# AI insights
st.subheader("🤖 AI Financial Insights")

if expenses > income and income > 0:
    st.error(
        "⚠️ Your expenses are higher than your income. "
        "Consider reducing discretionary spending."
    )

elif savings_rate >= 30:
    st.success(
        "✅ Excellent savings rate. "
        "Your spending is well controlled."
    )

elif savings_rate >= 15:
    st.info(
        "👍 Your savings rate is moderate. "
        "You can improve it by reducing unnecessary expenses."
    )

else:
    st.warning(
        "💡 Your savings rate is low. "
        "Review food, shopping, subscriptions and other "
        "non-essential expenses."
    )

if not category.empty:

    highest_category = category.index[0]
    highest_amount = category.iloc[0]

    st.write(
        f"**Highest spending category:** "
        f"{highest_category} — ₹{highest_amount:,.0f}"
    )

    if income > 0:

        percentage = (
            highest_amount / income * 100
        )

        if percentage > 15:

            st.write(
                f"💡 **Recommendation:** "
                f"{highest_category} represents approximately "
                f"{percentage:.1f}% of your income. "
                f"Consider setting a monthly limit."
            )

# Unusual transaction detection
st.subheader("🔎 Transaction Monitoring")

if len(expense_df) >= 3:

    mean_amount = expense_df["Amount"].mean()
    std_amount = expense_df["Amount"].std()

    threshold = mean_amount + (1.5 * std_amount)

    unusual = expense_df[
        expense_df["Amount"] > threshold
    ]

    if not unusual.empty:

        st.warning(
            "Potentially unusual transactions detected:"
        )

        display_columns = [
            column for column in [
                "Date",
                "Description",
                "Category",
                "Amount"
            ]
            if column in unusual.columns
        ]

        st.dataframe(
            unusual[display_columns],
            use_container_width=True
        )

    else:

        st.success(
            "No potentially unusual transactions detected."
        )

# Recommendations
st.subheader("💡 Recommended Monthly Actions")

actions = []

if savings_rate < 20:
    actions.append(
        "Try to increase savings toward at least 20% of income."
    )

if "Food" in category.index:
    food_amount = category["Food"]

    if food_amount > 3000:
        actions.append(
            "Review food and restaurant spending "
            "and consider setting a weekly budget."
        )

if "Shopping" in category.index:
    actions.append(
        "Review shopping purchases and postpone "
        "non-essential purchases when possible."
    )

if "Subscription" in category.index:
    actions.append(
        "Review recurring subscriptions and cancel "
        "services you rarely use."
    )

if not actions:
    actions.append(
        "Continue tracking transactions and review "
        "your financial dashboard regularly."
    )

for action in actions:
    st.write("• " + action)

st.divider()

st.caption(
    "AI Finance Controller — Internship Prototype | "
    "For educational purposes only, not financial advice."
)
