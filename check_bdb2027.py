"""Quick check: can Big Data Bowl 2027 tracking support the team-shape analysis?

Run from your project folder:  python check_bdb2027.py
Paste the printed output back into the chat.
"""
from pathlib import Path
import pandas as pd

DATA = Path("bdb2027")          # folder where you unzipped the 2027 files
FILE = DATA / "game_tracking_2025.csv"

print("Files:", sorted(p.name for p in DATA.glob("*.csv")))
df = pd.read_csv(FILE, nrows=2_000_000, low_memory=False)
print("\nColumns:", list(df.columns))
print("\nFirst rows:\n", df.head(3).to_string())

id_col = next(c for c in ["nfl_id", "nflId"] if c in df)
play = [c for c in ["game_id", "gameId", "play_id", "playId"] if c in df]
frame = next((c for c in ["frame_id", "frameId", "frame", "time"] if c in df), None)
print("\nRows with no player id (ball rows?):", df[id_col].isna().sum())
if frame:
    per_frame = df.groupby(play + [frame])[id_col].nunique()
    print("\nPlayers tracked per frame (want ~22):\n", per_frame.describe().round(1).to_string())
for c in ["club", "team", "team_abbr", "possession_team", "position"]:
    if c in df:
        print(f"\n{c} values:", df[c].value_counts().head(12).to_dict())
if "event" in df:
    print("\nEvents:", df["event"].dropna().unique()[:30].tolist())

pp = pd.read_csv(DATA / "player_play.csv", nrows=5)
print("\nplayer_play columns:", list(pp.columns))
if frame:
    plays = df.groupby(play)[id_col].nunique()
    print("\nPlayers tracked per play (whole play):\n", plays.describe().round(1).to_string())