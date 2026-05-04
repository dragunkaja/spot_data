# Spotify Listening Behavior Analysis

An exploratory data analysis of 120,000+ personal Spotify streams combined with Spotify Global Top 200 rankings. The core objective is to quantify algorithmic bias: does Spotify's Autoplay push mainstream hits, or does it organically mirror user taste?

## Key Findings
* **Algorithmic Neutrality:** The probability of hearing a global hit via Spotify's Autoplay (`trackdone`) is **19.07%**, which is statistically identical to manual user selection (`clickrow`) at **19.26%**.
* **Contextual Shifts:** Mainstream music consumption drops significantly when playback is controlled via external smart devices (`remote`), indicating a shift toward niche content outside the primary mobile/desktop UI.
* **Hit Density:** Popular tracks form a consistent baseline in the daily listening routine rather than spiking during specific hours.

## Methodology & Pipeline
* **Time-Series Alignment:** Used `pandas.merge_asof` to join asynchronous personal streaming logs (JSON) with external daily ranking datasets (CSV).
* **Feature Engineering:** Built custom metrics for skip rates, engagement, and a `discovery_type` classifier to separate niche exploration from mainstream autoplay.
* **Behavioral Segmentation:** Clustered listening sessions based on application triggers (`reason_start`, `reason_end`) to analyze user intent.

## Tech Stack
**Python** • **Pandas** • **NumPy** • **Matplotlib** • **Seaborn** • **Jupyter**

## Project Structure
```text
.
├── data/
│   ├── raw/                 # Raw JSON/CSV dumps (gitignored)
│   └── processed/           # Cleaned datasets
├── src/
│   ├── data_loader.py       # ETL and time-series merging
│   ├── analysis.py          # Feature engineering & metrics
│   └── visualization.py     # Custom plotting logic
└── notebooks/
    └── spotify_analysis.ipynb
