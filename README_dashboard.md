# ⚽ Football AI Analytics Dashboard

A presentation-layer dashboard built on top of the
[football_analysis](https://github.com/abdullahtarek/football_analysis) project.
**Zero changes to the existing AI/tracking pipeline.**

---

## Files Added

| File | Purpose |
|------|---------|
| `export_data.py` | Reads the tracking stubs and produces CSV files |
| `dashboard.py` | Full Streamlit dashboard |
| `requirements_dashboard.txt` | Python dependencies for the dashboard |

---

## Setup (Step-by-Step)

### 1 — Clone & set up the base project
```bash
git clone https://github.com/abdullahtarek/football_analysis.git
cd football_analysis
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2 — Copy dashboard files into the project folder
Place `export_data.py`, `dashboard.py`, and `requirements_dashboard.txt`
into the root of `football_analysis/`.

### 3 — Install dashboard dependencies
```bash
pip install -r requirements_dashboard.txt
```

### 4 — Run the base AI pipeline on your video
```bash
# Put your match video in input_videos/
python main.py
```
This generates the `stubs/track_stubs.pkl` file.

### 5 — Export tracking data to CSV
```bash
python export_data.py
```
Produces `match_stats.csv` and `possession_stats.csv` in the project root.

### 6 — Launch the dashboard
```bash
streamlit run dashboard.py
```
A browser tab opens automatically at `http://localhost:8501`.

---

## Dashboard Features

### 📊 Team Overview Tab
- Possession donut chart (Team 1 vs Team 2)
- Distance covered bar chart per team
- Speed zone distribution (Walking / Jogging / Running / Sprinting)
- Full player leaderboard with distance, speed, sprints

### 🏃 Player Analytics Tab
- Per-player KPIs (distance, avg/max speed, sprint %)
- Speed timeline with sprint threshold line
- Speed distribution histogram
- Radar chart: player vs team average
- Cumulative distance over match

### 🗺️ Tactical Map Tab
- Player heatmap overlaid on pitch (KDE density)
- Interactive pitch map — scrub through the match frame-by-frame
- Zone filter: click a spot and see which players are nearby
- Movement trail coloured by speed

### 📄 Export Report Tab
- One-click PDF report generation (possession + team + player tables)
- CSV data export (filtered by selected frame range)

---

## Notes

- If `match_stats.csv` is not found, the dashboard runs in **Demo Mode**
  with synthetic data so you can preview the layout immediately.
- The sprint speed threshold is adjustable in the sidebar (default 17 km/h).
- The frame-range slider lets you analyse specific phases of the match
  (e.g. first half only, last 10 minutes, etc.).
