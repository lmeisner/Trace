from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.data_utils import delete_entry, load_entries, save_entry
from src.insights import generate_insights

DATA_FILE = ROOT_DIR / "data" / "wellness_log.csv"

st.set_page_config(
    page_title="Trace",
    page_icon="◌",
    layout="wide",
)

st.title("Trace")
st.caption("Track the small choices that shape how you feel.")

entries = load_entries(DATA_FILE)

tab_log, tab_dashboard, tab_history = st.tabs(
    ["Daily check-in", "Dashboard", "History"]
)

with tab_log:
    st.subheader("How are you doing today?")

    with st.form("daily_check_in", clear_on_submit=True):
        left, middle, right = st.columns(3)

        with left:
            entry_date = st.date_input("Date", value=date.today())
            sleep_hours = st.number_input(
                "Sleep hours",
                min_value=0.0,
                max_value=24.0,
                value=8.0,
                step=0.25,
            )
            sleep_quality = st.slider("Sleep quality", 1, 5, 3)

        with middle:
            mood = st.slider("Mood", 1, 5, 3)
            energy = st.slider("Energy", 1, 5, 3)
            stress = st.slider("Stress", 1, 5, 3)

        with right:
            workout = st.selectbox(
                "Workout",
                ["None", "Walk", "Run", "Strength", "Cycling", "Yoga", "Sports", "Other"],
            )
            workout_minutes = st.number_input(
                "Workout minutes",
                min_value=0,
                max_value=600,
                value=0,
                step=5,
            )
            symptoms = st.text_input(
                "Symptoms",
                placeholder="Headache, soreness, congestion...",
            )

        notes = st.text_area(
            "Notes",
            placeholder="What affected your day?",
        )

        submitted = st.form_submit_button("Save check-in", use_container_width=True)

        if submitted:
            save_entry(
                DATA_FILE,
                {
                    "date": entry_date,
                    "sleep_hours": sleep_hours,
                    "sleep_quality": sleep_quality,
                    "mood": mood,
                    "energy": energy,
                    "stress": stress,
                    "workout": workout,
                    "workout_minutes": workout_minutes,
                    "symptoms": symptoms.strip(),
                    "notes": notes.strip(),
                },
            )
            st.success("Your check-in was saved.")
            st.rerun()

with tab_dashboard:
    if entries.empty:
        st.info("Add your first daily check-in to build your dashboard.")
    else:
        latest = entries.sort_values("date").iloc[-1]

        metric_one, metric_two, metric_three, metric_four = st.columns(4)
        metric_one.metric("Latest mood", f"{int(latest['mood'])}/5")
        metric_two.metric("Latest energy", f"{int(latest['energy'])}/5")
        metric_three.metric("Latest stress", f"{int(latest['stress'])}/5")
        metric_four.metric("Latest sleep", f"{latest['sleep_hours']:.1f} hrs")

        st.subheader("Recent trends")

        trend_data = entries.melt(
            id_vars="date",
            value_vars=["mood", "energy", "stress", "sleep_quality"],
            var_name="metric",
            value_name="score",
        )

        trend_chart = px.line(
            trend_data,
            x="date",
            y="score",
            color="metric",
            markers=True,
            labels={
                "date": "Date",
                "score": "Score",
                "metric": "Metric",
            },
        )
        trend_chart.update_yaxes(range=[1, 5])
        st.plotly_chart(trend_chart, use_container_width=True)

        sleep_chart = px.bar(
            entries,
            x="date",
            y="sleep_hours",
            labels={"date": "Date", "sleep_hours": "Sleep hours"},
        )
        st.plotly_chart(sleep_chart, use_container_width=True)

        st.subheader("Patterns Trace noticed")
        for insight in generate_insights(entries):
            st.write(f"• {insight}")

with tab_history:
    if entries.empty:
        st.info("Your saved check-ins will appear here.")
    else:
        display_entries = entries.copy().reset_index(drop=True)
        display_entries["date"] = display_entries["date"].dt.strftime("%Y-%m-%d")

        st.dataframe(
            display_entries,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Delete an entry")
        selected_index = st.selectbox(
            "Choose a row",
            options=list(range(len(display_entries))),
            format_func=lambda index: (
                f"{index}: {display_entries.loc[index, 'date']} — "
                f"mood {display_entries.loc[index, 'mood']}/5"
            ),
        )

        if st.button("Delete selected entry"):
            delete_entry(DATA_FILE, selected_index)
            st.success("Entry deleted.")
            st.rerun()
