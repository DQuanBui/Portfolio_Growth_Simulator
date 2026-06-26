import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portfolio Growth Simulator",
    page_icon="📈",
    layout="wide"
)

def calculate_projection(starting_value, annual_contribution, growth_rate, years):
    rows = []
    portfolio_value = starting_value

    for year in range(1, years + 1):
        beginning_value = portfolio_value
        investment_gain = beginning_value * (growth_rate / 100)
        ending_value = beginning_value + investment_gain + annual_contribution

        rows.append({
            "Year": year,
            "Beginning Value": beginning_value,
            "Annual Contribution": annual_contribution,
            "Investment Gain": investment_gain,
            "Ending Value": ending_value
        })

        portfolio_value = ending_value

    return pd.DataFrame(rows)

def money(value):
    return f"${value:,.0f}"

st.title("📈 Portfolio Growth Simulator")

st.write(
    "This app helps you estimate how a portfolio may grow over time based on "
    "starting value, annual contributions, expected return, and investment time horizon."
)

st.sidebar.header("Input Assumptions")

starting_value = st.sidebar.number_input(
    "Starting Portfolio Value ($)",
    min_value=0,
    value=100000,
    step=5000
)

annual_contribution = st.sidebar.number_input(
    "Annual Contribution ($)",
    min_value=0,
    value=10000,
    step=1000
)

growth_rate = st.sidebar.slider(
    "Expected Annual Growth Rate (%)",
    min_value=-20.0,
    max_value=25.0,
    value=7.0,
    step=0.5
)

years = st.sidebar.slider(
    "Investment Time Horizon (Years)",
    min_value=1,
    max_value=40,
    value=10
)

scenario = st.sidebar.selectbox(
    "Scenario",
    ["Base Case", "Conservative", "Optimistic"]
)

if scenario == "Conservative":
    scenario_growth_rate = growth_rate - 2
elif scenario == "Optimistic":
    scenario_growth_rate = growth_rate + 2
else:
    scenario_growth_rate = growth_rate

df = calculate_projection(
    starting_value,
    annual_contribution,
    scenario_growth_rate,
    years
)

final_value = df["Ending Value"].iloc[-1]
total_contributions = annual_contribution * years
total_invested = starting_value + total_contributions
total_gain = final_value - total_invested

if total_invested > 0:
    total_return = total_gain / total_invested * 100
else:
    total_return = 0

st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Final Value", money(final_value))
col2.metric("Total Invested", money(total_invested))
col3.metric("Investment Gain", money(total_gain))
col4.metric("Total Return", f"{total_return:.1f}%")

st.subheader("Portfolio Growth Chart")

chart_df = df[["Year", "Ending Value"]].set_index("Year")
st.line_chart(chart_df)

st.subheader("Annual Investment Gain")

gain_df = df[["Year", "Investment Gain"]].set_index("Year")
st.bar_chart(gain_df)

st.subheader("Year-by-Year Projection")

display_df = df.copy()
display_df["Beginning Value"] = display_df["Beginning Value"].apply(money)
display_df["Annual Contribution"] = display_df["Annual Contribution"].apply(money)
display_df["Investment Gain"] = display_df["Investment Gain"].apply(money)
display_df["Ending Value"] = display_df["Ending Value"].apply(money)

st.dataframe(display_df, use_container_width=True)

csv = df.to_csv(index=False)

st.download_button(
    label="Download Projection as CSV",
    data=csv,
    file_name="portfolio_projection.csv",
    mime="text/csv"
)

st.subheader("Interpretation")

st.write(
    f"In the {scenario} scenario, the portfolio grows from "
    f"{money(starting_value)} to {money(final_value)} over {years} years."
)

st.write(
    f"This uses an annual growth rate of {scenario_growth_rate:.1f}% "
    f"and an annual contribution of {money(annual_contribution)}."
)

st.info(
    "This app is for learning and demonstration only. It is not financial advice."
)