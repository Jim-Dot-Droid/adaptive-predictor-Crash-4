# Crash Game Predictor (Adaptive + Accuracy)

This Streamlit app predicts whether the next multiplier in a crash game will be above or under 2.0 (200%) based on your manually entered history.

## Features
- Manual input of multipliers after each crash round.
- Three adaptive prediction models:
  1. **Frequency**: Uses full history ratio.
  2. **Moving Average**: Based on recent N rounds.
  3. **Markov Chain**: Predicts based on last state transitions.
- Displays recent history (last 10 values).
- Tracks prediction accuracy automatically.
- Reset option to clear history and stats.

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   streamlit run app.py
   ```

## Deployment
- Push this repository to GitHub.
- Deploy on Streamlit Cloud.
