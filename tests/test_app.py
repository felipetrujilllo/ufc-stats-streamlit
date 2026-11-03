from streamlit.testing.v1 import AppTest


def test_app_renders_and_handles_empty_filter():
    at = AppTest.from_file("app.py").run(timeout=30)
    assert not at.exception
    assert len(at.get("plotly_chart")) == 2
    at.sidebar.multiselect[0].set_value([]).run()
    assert at.warning
