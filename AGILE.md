# AGILE Process

The project uses a lightweight version of **Scrum**: a product backlog of user stories, two short sprints, a definition of done, and a retrospective. Each user story is tracked as a GitHub Issue, and the commit that finishes the story closes it (`Closes #n`). The Issues tab and the commit history are the sprint board.

## Product backlog (user stories)

| # | User story | Acceptance criteria | Points | Sprint |
|---|---|---|---|---|
| 1 | As a user, I want the app to load a real dataset so that I can explore real data. | A CSV in `data/` is loaded and cached, and `requirements.txt` lists all dependencies. | 2 | 1 |
| 2 | As a user, I want sidebar filters (year, continent, log scale) so that I can focus on what interests me. | A slider, multiselect, and checkbox filter all content, and an empty selection shows a warning instead of an error. | 3 | 1 |
| 3 | As a user, I want interactive Plotly charts so that I can see trends at a glance. | A scatter chart and a line chart, each with a title, axis labels, legend, and hover info. | 5 | 1 |
| 4 | As a user, I want Overview, Data Display, and Insights sections with explanations so that I understand what I'm looking at. | The three sections have explanatory text, metrics, and insights that update with the filters. | 3 | 2 |
| 5 | As the instructor, I want a README and a public deployment so that I can review and use the app. | The README covers purpose, dataset, and instructions, and the app is live on Streamlit Community Cloud. | 2 | 2 |

## Sprints

**Sprint 1 (core features).** Goal: a working app with data, filters, and charts. Stories #1–#3, 10 points.

**Sprint 2 (polish and delivery).** Goal: make the app understandable and ship it. Stories #4–#5, 5 points.

## Definition of done

- The app runs with `streamlit run app.py` without errors or deprecation warnings.
- `pytest` passes. The test renders the app, checks that both charts appear, and checks the empty-filter case.
- The change is committed, and the commit closes its GitHub Issue.

## Retrospective

- **Went well:** Small, testable stories made it easy to finish each feature in one commit.
- **To improve:** Streamlit deprecated `use_container_width`. The smoke test caught it, so pinning minimum versions in `requirements.txt` was the right call.
- **Next (Project 2):** Add AI and API features on top of this dashboard, for example a "describe this chart" button.
