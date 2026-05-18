# TV Show Mental Health Impact Analyser

A machine learning system that classifies TV shows by their likely emotional and mental health impact on viewers. Built using Python, NLP, and Random Forest — trained on 8,385 real IMDb reviews across 50 shows.

Unlike standard recommendation systems that focus on entertainment quality, this tool predicts how a show might affect your **mood and mental wellbeing**, classifying each show into one of four categories:

| Category | Description |
|---|---|
|  Positive | Uplifting, comforting, feel-good content |
|  Balanced | Mixed emotional tones, manageable for most viewers |
|  Intense | Gripping and emotionally demanding but not distressing |
|  Heavy | Dark, traumatic, or psychologically draining content |

---

## Demo

The system is deployed as an interactive Streamlit dashboard with five pages:
- **Home** — project overview and category guide
- **Analyse Show** — search any show and view its classification, sentiment score, and supporting viewer reviews
- **All Shows** — browse all 50 shows by category with a bar chart breakdown
- **Why It Matters** — the research behind TV and mental health
- **About Model** — model performance, precision scores, and the key TF-IDF finding

---

## Results

| Metric | Value |
|---|---|
| Overall Accuracy | 77% |
| Positive Precision | 97% |
| Balanced Precision | 70% |
| Intense Precision | 65% |
| Heavy Precision | 68% |
| Reviews Analysed | 8,385 |
| Shows Covered | 50 |
| Features Per Review | 115 |

**Key finding:** TF-IDF features alone contributed a **33 percentage point** accuracy improvement — removing TF-IDF dropped accuracy from 77% to 44%, confirming that the specific vocabulary viewers use matters far more than sentiment polarity alone.

---

## Tech Stack

- **Language:** Python 3
- **Environment:** Google Colab
- **NLP:** VADER (vaderSentiment), text2emotion
- **ML:** scikit-learn (Random Forest, TF-IDF, StandardScaler)
- **Data:** pandas, NumPy, scipy
- **Dashboard:** Streamlit, Plotly
- **Deployment:** ngrok
- **Serialisation:** pickle

---

## How It Works

1. **Data Collection** — IMDb user reviews were collected manually across 50 TV shows after automated approaches (Kaggle dataset, TMDB API, BeautifulSoup scraping) all failed to produce usable data
2. **Feature Extraction** — each review is processed through VADER (4 sentiment scores), text2emotion (5 emotion dimensions), a mental health keyword counter, review length/punctuation features, and TF-IDF — producing 115 features per review
3. **Model Training** — a Random Forest classifier (200 trees, max depth 20) is trained on an 80/20 train-test split
4. **Show Classification** — predictions are made at the review level then aggregated by majority vote across all reviews for a show
5. **Dashboard** — results are served through a Streamlit dashboard deployed via ngrok

---

## Challenges Solved

**Class imbalance** — the model initially classified children's shows like PAW Patrol as Intense because it had never seen genuinely wholesome content. Fixed through anchor data injection — hand-writing representative reviews for underrepresented categories (Bluey, Great British Bake Off, Parks and Recreation) to give the model clear examples of Positive content.

**VADER limitation** — VADER measures how positively viewers talk about a show, not the show's emotional weight. Chernobyl gets glowing reviews despite being deeply traumatic. Fixed by expanding the mental health keyword list with Heavy-specific vocabulary (devastating, haunting, traumatic, harrowing) and implementing a post-training override system.


---

## Project Structure

```
tv-show-mental-health-analyser/
│
├── Copy_of_dissertation_project.ipynb   # Full pipeline — data processing, training, evaluation
├── dashboard.py                          # Streamlit dashboard
└── README.md
```

---

## Running the Dashboard

The system runs in Google Colab. Open the notebook, run all cells in order, then launch the dashboard using the ngrok cell at the end. A public URL will be printed that opens the dashboard in any browser.

---
##Improvements to make

** Accuracy needs to improve. Alot of shows were placed into the wrong category and required forced repositions. Need to find a new library to improve this

## About

Final year undergraduate major project — BSc Data and Analytical Science, Anglia Ruskin University (2024–2025).

Connect on [LinkedIn](www.linkedin.com/in/obinna-oji-aa406b316) | [GitHub](https://github.com/ObinnaOji)
