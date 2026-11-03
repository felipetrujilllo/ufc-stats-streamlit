import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Streamlit Assignment App", page_icon="🌍", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("data/gapminder.csv")


df = load_data()

# Sidebar: user input
st.sidebar.header("Filters")
year = st.sidebar.slider("Year", int(df.year.min()), int(df.year.max()), 2007, step=5)
continents = st.sidebar.multiselect(
    "Continents", sorted(df.continent.unique()), default=sorted(df.continent.unique())
)
log_x = st.sidebar.checkbox("Log scale for GDP per capita", value=True)

filtered = df[(df.year == year) & (df.continent.isin(continents))]

# Overview
st.title("🌍 Streamlit Assignment App")
st.header("Overview")
st.write(
    "This app explores the **Gapminder** dataset: life expectancy, population, and GDP per "
    "capita for 142 countries from 1952 to 2007. Use the filters in the sidebar to choose a "
    "year and continents, and every section below updates."
)

if filtered.empty:
    st.warning("Select at least one continent to see data.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Countries", filtered.country.nunique())
c2.metric("Avg life expectancy", f"{filtered.lifeExp.mean():.1f} yrs")
c3.metric("Total population", f"{filtered['pop'].sum() / 1e9:.2f} B")

# Data Display
st.header("Data Display")
st.subheader(f"Wealth vs. health in {year}")
st.write("Each bubble is a country. Bubble size is population; hover for details.")
fig = px.scatter(
    filtered,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=log_x,
    size_max=60,
    title=f"Life Expectancy vs. GDP per Capita ({year})",
    labels={"gdpPercap": "GDP per capita (US$, inflation-adjusted)", "lifeExp": "Life expectancy (years)", "continent": "Continent"},
)
st.plotly_chart(fig, width="stretch")

st.subheader("Life expectancy over time by continent")
trend = df[df.continent.isin(continents)].groupby(["year", "continent"], as_index=False).lifeExp.mean()
fig2 = px.line(
    trend,
    x="year",
    y="lifeExp",
    color="continent",
    markers=True,
    title="Average Life Expectancy by Continent, 1952–2007",
    labels={"year": "Year", "lifeExp": "Average life expectancy (years)", "continent": "Continent"},
)
st.plotly_chart(fig2, width="stretch")

with st.expander("Show raw data"):
    st.dataframe(filtered.sort_values("lifeExp", ascending=False), width="stretch", hide_index=True)

# Insights
st.header("Insights")
top = filtered.loc[filtered.lifeExp.idxmax()]
low = filtered.loc[filtered.lifeExp.idxmin()]
corr = filtered.gdpPercap.corr(filtered.lifeExp)
st.markdown(
    f"""
- **Highest life expectancy in {year}:** {top.country} ({top.lifeExp:.1f} years).
- **Lowest life expectancy in {year}:** {low.country} ({low.lifeExp:.1f} years).
- **GDP vs. life expectancy correlation:** {corr:.2f}. Richer countries tend to live longer,
  but the curve flattens at high incomes, which the log scale makes easy to see.
- Life expectancy rose on every continent over the period; Africa's gains slowed in the
  1990s, a period that overlaps with the HIV/AIDS epidemic.
"""
)
st.caption("Data: Gapminder Foundation (gapminder.org), via plotly.express.data.gapminder().")
