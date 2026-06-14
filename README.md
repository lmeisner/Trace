# Trace

Trace is a personal wellness journal that connects wearable data, subjective reflections, habits, and goals over time.

Rather than showing health metrics in isolation, Trace is designed to identify the patterns and tradeoffs that shape physical, mental, and productive well-being.

## Problem

Wearable apps measure sleep, recovery, and activity, while journals capture mood, habits, and personal context. These sources are usually separated, making it difficult to understand why changes happen or how different wellness goals interact.

## Planned Features

- Import sleep and recovery data from Oura
- Record mood, energy, brain fog, stress, and productivity
- Track customizable wellness goals
- Generate weekly wellness summaries
- Compare subjective feelings with physiological recovery
- Identify delayed relationships between habits and outcomes
- Detect conflicts between competing goals
- Protect personal information through local storage and synthetic demo data

## Initial Development Roadmap

1. Design the daily journal data model
2. Build a manual daily check-in
3. Store and display previous entries
4. Import Oura data
5. Combine journal and wearable data by date
6. Create a weekly dashboard
7. Develop a basic pattern-discovery engine

## Technology

- Python
- pandas
- Streamlit
- Plotly or Matplotlib
- SQLite
- scikit-learn

## Privacy

Personal health information, journal entries, and API credentials will not be committed to this repository. Public demonstrations will use synthetic data.

## Current Status

Trace is currently in the planning and early development stage.