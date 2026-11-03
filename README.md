# UFC Fight Explorer

An interactive Streamlit app for exploring how UFC fights end (knockout, submission, or decision) and how that has changed from 1994 to 2026.

**Live app:** _add your Streamlit Community Cloud URL here_

## Purpose

The app shows how to visualize and interact with a real dataset in Python. It answers three questions: how UFC fights usually end, how finish methods differ between weight classes, and whether fights have gone to the judges more often over time.

## Dataset

Two CSVs in [`data/`](data/) come from **ufcstats.com**, the UFC's official stats site, through the public [scrape_ufc_stats](https://github.com/Greco1899/scrape_ufc_stats) project. The app merges them on the event name.

| File | Rows | Columns used |
|---|---|---|
| [`ufc_fight_results.csv`](data/ufc_fight_results.csv) | ~9,000 fights | `EVENT`, `BOUT` (fighter names), `OUTCOME` (W/L, L/W, draw, no contest), `WEIGHTCLASS`, `METHOD`, `ROUND` |
| [`ufc_event_details.csv`](data/ufc_event_details.csv) | ~800 events | `EVENT`, `DATE` |

When the app loads, it groups methods into KO/TKO, Submission, Decision, and Other. It also folds title and non-title bouts into one weight class and finds the winner from `OUTCOME`. Three events have no date in the events file, so their fights are left out.

## How to use

1. In the **sidebar**, pick one or more **Weight classes**.
2. Drag the **Years** slider to set a range.
3. Tick **Title fights only** to see championship bouts only.
4. Untick **Show finish methods as a percentage** to see fight counts instead.
5. Read the sections from top to bottom:
   - **Overview**: what the app does, plus summary metrics (fights, finish rate, events).
   - **Data Display**: a bar chart of outcomes by year and a bar chart of outcomes by weight class (both Plotly). Hover over a bar for details, click a legend item to hide that method, and drag on a chart to zoom. Open **Show raw data** to see the fights table.
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

The project was built in three short Scrum-style sprints. Each user story is a GitHub Issue that a commit closes. See [AGILE.md](AGILE.md) for the backlog, sprints, and retrospective.
