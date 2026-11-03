import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="UFC Fight Explorer", page_icon="", layout="wide")

DIVISIONS = [
    "Flyweight", "Bantamweight", "Featherweight", "Lightweight", "Welterweight",
    "Middleweight", "Light Heavyweight", "Heavyweight", "Women's Strawweight",
    "Women's Flyweight", "Women's Bantamweight", "Women's Featherweight",
]

def method_group(m):
    if m.startswith("Decision"):
        return "Decision"
    if "KO" in m:
        return "KO/TKO"
    if m == "Submission":
        return "Submission"
    return "Other (DQ, overturned, etc.)"

@st.cache_data
def load_data():
    fights = pd.read_csv("data/ufc_fight_results.csv").apply(lambda c: c.str.strip() if pd.api.types.is_string_dtype(c) else c)
    events = pd.read_csv("data/ufc_event_details.csv").apply(lambda c: c.str.strip())
    events = events.drop_duplicates("EVENT")[["EVENT", "DATE"]]
    # A handful of events are missing from the events file; they have no date, so they i dropped them.
    df = fights.merge(events, on="EVENT")
    df["date"] = pd.to_datetime(df.DATE, format="%B %d, %Y")
    df["year"] = df.date.dt.year
    df["title_fight"] = df.WEIGHTCLASS.str.contains("Title")
    division = df.WEIGHTCLASS.str.replace("UFC ", "").str.replace(" Title", "").str.replace(" Bout", "")
    df["division"] = division.where(division.isin(DIVISIONS), "Other (open, catch, tournament)")
    df["method"] = df.METHOD.map(method_group)
    fighters = df.BOUT.str.split(" vs. ", n=1, expand=True)
    df["winner"] = fighters[0].where(df.OUTCOME == "W/L", fighters[1].where(df.OUTCOME == "L/W"))
    return df[["date", "year", "EVENT", "BOUT", "division", "title_fight", "method", "METHOD", "ROUND", "winner"]]


df = load_data()

# Sidebar: user input
st.sidebar.header("Filters")
divisions = st.sidebar.multiselect("Weight classes", DIVISIONS, default=DIVISIONS)
years = st.sidebar.slider("Years", int(df.year.min()), int(df.year.max()), (2010, int(df.year.max())))
titles_only = st.sidebar.checkbox("Title fights only")
as_percent = st.sidebar.checkbox("Show finish methods as a percentage", value=True)

filtered = df[df.division.isin(divisions) & df.year.between(*years)]
if titles_only:
    filtered = filtered[filtered.title_fight]

# Overview
st.title("UFC Fight Stats")
st.header("Overview")
st.write(
    f"This app explores **every UFC fight result from {df.year.min()} to {df.year.max()}** "
    f"({len(df):,} fights). Use the sidebar to choose weight classes and years, and every section below "
    "updates. The main question: **how do UFC fights end, and has that changed over time?**"
)

if filtered.empty:
    st.warning("No fights match these filters. Select at least one weight class.")
    st.stop()

finishes = filtered[filtered.method.isin(["KO/TKO", "Submission"])]
c1, c2, c3 = st.columns(3)
c1.metric("Fights", f"{len(filtered):,}")
c2.metric("Finish rate (KO/TKO or submission)", f"{len(finishes) / len(filtered):.0%}")
c3.metric("Events", filtered.EVENT.nunique())

# Data Display
st.header("Data Display")
st.subheader("How fights end, year by year")
st.write("Each bar is one year of fights, split by how they ended. Click a legend item to hide that method.")
by_year = filtered.groupby(["year", "method"], as_index=False).size()
fig = px.bar(
    by_year,
    x="year",
    y="size",
    color="method",
    title=f"UFC Fight Outcomes by Year ({years[0]}–{years[1]})",
    labels={"year": "Year", "size": "Share of fights (%)" if as_percent else "Number of fights", "method": "Method"},
)
fig.update_layout(barnorm="percent" if as_percent else "")
st.plotly_chart(fig)

st.subheader("Finish methods by weight class")
st.write("Lighter divisions go to the judges more often; heavyweights get knocked out more.")
by_div = filtered.groupby(["division", "method"], as_index=False).size()
fig2 = px.bar(
    by_div,
    x="size",
    y="division",
    color="method",
    orientation="h",
    category_orders={"division": DIVISIONS + ["Other (open, catch, tournament)"]},
    title="UFC Fight Outcomes by Weight Class",
    labels={"division": "Weight class", "size": "Share of fights (%)" if as_percent else "Number of fights", "method": "Method"},
)
fig2.update_layout(barnorm="percent" if as_percent else "")
st.plotly_chart(fig2)

with st.expander("Show raw data"):
    st.dataframe(filtered.sort_values("date", ascending=False), width="stretch", hide_index=True)

st.header("Insights")
ko_by_div = filtered.groupby("division").method.apply(lambda m: (m == "KO/TKO").mean())
top_winner = filtered.winner.value_counts()
st.markdown(
    f"""
- **Most common outcome:** {filtered.method.mode()[0]} ({filtered.method.value_counts(normalize=True).iloc[0]:.0%} of fights).
- **Highest KO/TKO rate:** {ko_by_div.idxmax()} ({ko_by_div.max():.0%} of its fights).
- **Average round a finish happens in:** {finishes.ROUND.mean():.1f}. Most knockouts and submissions come early.
- **Most wins in this selection:** {top_winner.index[0]} ({top_winner.iloc[0]} wins).
- Over the years, more fights have gone to decision as fighters became more well-rounded.
  Compare the early 2000s with recent years in the first chart.
"""
)
st.caption("Data: ufcstats.com, from: scrape_ufc_stats project (github.com/Greco1899/scrape_ufc_stats).")
