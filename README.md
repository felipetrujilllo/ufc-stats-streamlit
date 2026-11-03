# Streamlit Assignment App

An interactive Streamlit app for exploring how wealth, health, and population have changed around the world from 1952 to 2007.

**Live app:** _add your Streamlit Community Cloud URL here_

## Purpose

The app shows how to visualize and interact with a real dataset in Python. It answers three questions: how GDP per capita relates to life expectancy, how that relationship differs between continents, and how life expectancy has changed over time.

## Dataset

[`data/gapminder.csv`](data/gapminder.csv) holds 1,704 rows from the **Gapminder** dataset (gapminder.org), which ships with Plotly as `plotly.express.data.gapminder()`. It covers 142 countries, every 5 years from 1952 to 2007.

| Column | Meaning |
|---|---|
| `country`, `continent`, `iso_alpha` | Country name, continent, ISO 3-letter code |
| `year` | 1952–2007, in 5-year steps |
| `lifeExp` | Life expectancy at birth (years) |
| `pop` | Population |
| `gdpPercap` | GDP per capita (inflation-adjusted US$) |

## How to use

1. In the **sidebar**, pick a **Year** with the slider.
2. Choose one or more **Continents** in the multiselect.
3. Turn the **log scale** checkbox on or off for the GDP axis.
4. Read the sections from top to bottom:
   - **Overview**: what the app does, plus summary metrics.
   - **Data Display**: a bubble chart of GDP vs. life expectancy and a line chart of life expectancy over time (both Plotly). Hover over a point for details. Click a legend item to hide that continent, and drag on the chart to zoom. Open **Show raw data** to see the table.
   - **Insights**: findings that update with your filters.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

To run the tests:

```bash
pip install pytest
pytest
```

## Deploy

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), click **Create app**, and select this repo with branch `main` and main file `app.py`.
3. Copy the public URL into the **Live app** line at the top of this README.

## Project management

The project was built in two short Scrum-style sprints. Each user story is a GitHub Issue that a commit closes. See [AGILE.md](AGILE.md) for the backlog, sprints, and retrospective.
