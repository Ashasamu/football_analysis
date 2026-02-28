"""
export_data.py
==============
Run this ONCE after main.py has processed your video.
It reads the tracking stubs and produces two CSV files:
  - match_stats.csv       (frame-by-frame player data)
  - possession_stats.csv  (per-team possession counts)

Usage:
    python export_data.py
"""

import pickle
import pandas as pd
import os

STUB_PATH = "stubs/track_stubs.pkl"
OUT_STATS = "match_stats.csv"
OUT_POSS  = "possession_stats.csv"


def load_stubs(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Could not find '{path}'.\n"
            "Make sure you have run main.py first so that the stubs/ folder is populated."
        )
    with open(path, "rb") as f:
        return pickle.load(f)


def export(stub_path: str = STUB_PATH):
    print(f"Loading tracking stubs from '{stub_path}' …")
    tracks = load_stubs(stub_path)

    player_rows = []
    possession_counts = {1: 0, 2: 0}

    player_frames  = tracks.get("players", [])
    ball_control   = tracks.get("team_ball_control", [])

    for frame_num, player_track in enumerate(player_frames):
        for player_id, info in player_track.items():
            team_id = info.get("team")
            if team_id is None:
                continue

            bbox = info.get("bbox", [0, 0, 0, 0])
            cx   = (bbox[0] + bbox[2]) / 2
            cy   = (bbox[1] + bbox[3]) / 2

            # Prefer perspective-transformed coordinates when available
            coords = info.get("position_transformed") or info.get("coord_transformed")
            x_m = coords[0] if coords else cx
            y_m = coords[1] if coords else cy

            player_rows.append({
                "frame":     frame_num,
                "player_id": int(player_id),
                "team":      int(team_id),
                "team_label": f"Team {team_id}",
                "x_px":      round(cx, 2),
                "y_px":      round(cy, 2),
                "x_m":       round(float(x_m), 3),
                "y_m":       round(float(y_m), 3),
                "speed":     round(float(info.get("speed", 0)), 2),
                "distance":  round(float(info.get("distance", 0)), 3),
            })

        # Possession
        if frame_num < len(ball_control):
            ctrl = int(ball_control[frame_num])
            if ctrl in possession_counts:
                possession_counts[ctrl] += 1

    # ── Player stats ──────────────────────────────────────────────
    df = pd.DataFrame(player_rows)
    df.to_csv(OUT_STATS, index=False)
    print(f"  ✔ Saved {len(df):,} rows  →  {OUT_STATS}")

    # ── Possession summary ────────────────────────────────────────
    pos_df = pd.DataFrame([
        {"team": f"Team {k}", "frames": v}
        for k, v in possession_counts.items()
    ])
    pos_df.to_csv(OUT_POSS, index=False)
    print(f"  ✔ Possession summary   →  {OUT_POSS}")
    print("Done! You can now run:  streamlit run dashboard.py")


if __name__ == "__main__":
    export()
