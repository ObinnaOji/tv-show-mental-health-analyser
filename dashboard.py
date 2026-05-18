
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="TV Show Mood Impact Analyser",
    page_icon="TV",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #0f1117;
    color: #e8e8e8;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #2a2f3e;
}

[data-testid="stSidebar"] .stRadio label {
    color: #b0b8cc !important;
    font-size: 0.9rem;
    padding: 6px 0;
}

[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.02em;
    margin-bottom: 1.5rem;
}

/* ── Headings ── */
h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.6rem !important;
    font-weight: 400 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em;
    line-height: 1.15 !important;
}

h2 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.6rem !important;
    font-weight: 400 !important;
    color: #d4d8e8 !important;
}

h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8892a4 !important;
}

/* ── Category Cards ── */
.category-card {
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    border-left: 4px solid;
    background: #161b27;
}
.card-positive  { border-color: #4ecdc4; background: linear-gradient(135deg, #161b27 60%, #0d2e2c); }
.card-balanced  { border-color: #5b9bd5; background: linear-gradient(135deg, #161b27 60%, #0d1e2e); }
.card-intense   { border-color: #f4a261; background: linear-gradient(135deg, #161b27 60%, #2e1e0d); }
.card-heavy     { border-color: #e05c6f; background: linear-gradient(135deg, #161b27 60%, #2e0d15); }

.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    font-weight: 400;
    color: #ffffff;
    margin-bottom: 4px;
}
.card-desc {
    font-size: 0.85rem;
    color: #8892a4;
    margin: 0;
}

/* ── Mood Badge ── */
.mood-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.badge-Positive { background: #0d2e2c; color: #4ecdc4; border: 1px solid #4ecdc4; }
.badge-Balanced { background: #0d1e2e; color: #5b9bd5; border: 1px solid #5b9bd5; }
.badge-Intense  { background: #2e1e0d; color: #f4a261; border: 1px solid #f4a261; }
.badge-Heavy    { background: #2e0d15; color: #e05c6f; border: 1px solid #e05c6f; }

/* ── Show Title ── */
.show-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #ffffff;
    margin-bottom: 8px;
}

/* ── Stat Box ── */
.stat-box {
    background: #161b27;
    border: 1px solid #2a2f3e;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
}
.stat-number {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #ffffff;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Info Panel ── */
.info-panel {
    background: #161b27;
    border: 1px solid #2a2f3e;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 16px;
}
.info-panel p {
    color: #b0b8cc;
    font-size: 0.9rem;
    line-height: 1.7;
    margin: 0;
}

/* ── Divider ── */
.custom-divider {
    border: none;
    border-top: 1px solid #2a2f3e;
    margin: 24px 0;
}

/* ── Show Row ── */
.show-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: #161b27;
    border-radius: 8px;
    margin-bottom: 6px;
    border: 1px solid #2a2f3e;
}
.show-row-title {
    font-weight: 500;
    color: #e8e8e8;
    font-size: 0.9rem;
}
.show-row-meta {
    font-size: 0.8rem;
    color: #8892a4;
}

/* ── Metric overrides ── */
[data-testid="stMetric"] {
    background: #161b27;
    border: 1px solid #2a2f3e;
    border-radius: 10px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { color: #8892a4 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"] { color: #ffffff !important; font-family: 'DM Serif Display', serif !important; font-size: 1.8rem !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #161b27 !important;
    border: 1px solid #2a2f3e !important;
    color: #e8e8e8 !important;
    border-radius: 8px !important;
}

/* ── Button ── */
.stButton > button {
    background: #ffffff !important;
    color: #0f1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 10px 28px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #161b27 !important;
    border: 1px solid #2a2f3e !important;
    border-radius: 8px !important;
    color: #b0b8cc !important;
}

/* ── Alert boxes ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    border-left-width: 4px !important;
}

/* ── Radio buttons ── */
.stRadio > div { gap: 4px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a2f3e; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    shows = pd.read_csv('show_summaries.csv')
    return shows

shows_df = load_data()

category_colors = {
    'Positive': '#4ecdc4',
    'Balanced': '#5b9bd5',
    'Intense':  '#f4a261',
    'Heavy':    '#e05c6f'
}

category_descriptions = {
    'Positive': 'Uplifting content that supports emotional wellbeing and stress relief.',
    'Balanced': 'Mixed emotional content — engaging but manageable for most viewers.',
    'Intense':  'Emotionally demanding viewing. Watch when you have the energy for it.',
    'Heavy':    'Dark, challenging content. Viewer discretion advised.',
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Mood Impact Analyser")
st.sidebar.markdown("<hr style='border-color:#2a2f3e; margin: 8px 0 20px 0'>", unsafe_allow_html=True)
page = st.sidebar.radio("", ["Home", "Analyse Show", "All Shows", "Why It Matters", "About Model"])

st.sidebar.markdown("<hr style='border-color:#2a2f3e; margin: 20px 0 16px 0'>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='font-size:0.75rem; color:#4a5568; line-height:1.6;'>
    <strong style='color:#6b7280'>Dataset</strong><br>
    8,385 reviews &bull; 50 shows<br><br>
    <strong style='color:#6b7280'>Model</strong><br>
    Random Forest &bull; 77% accuracy<br><br>
    <strong style='color:#6b7280'>Categories</strong><br>
    Positive &bull; Balanced &bull; Intense &bull; Heavy
</div>
""", unsafe_allow_html=True)

# ── HOME ─────────────────────────────────────────────────────────────────────
if page == "Home":
    st.markdown("<h1>TV Show<br><em>Mental Health Impact Analyser</em></h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2a2f3e; margin: 20px 0 28px 0'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-panel'>
    <p>This tool uses machine learning to classify TV shows by their likely emotional and mental health impact on viewers.
    Unlike standard recommendation systems that focus on entertainment quality, this classifier analyses thousands of
    authentic viewer reviews to predict how a show might affect your <strong style='color:#e8e8e8'>mood and mental wellbeing</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-number'>{len(shows_df)}</div>
            <div class='stat-label'>Shows Analysed</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-number'>8,385</div>
            <div class='stat-label'>Reviews Processed</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-box'>
            <div class='stat-number'>77%</div>
            <div class='stat-label'>Model Accuracy</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><h3>Mood Impact Categories</h3><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='category-card card-positive'>
            <div class='card-title'>Positive</div>
            <p class='card-desc'>Feel-good content, uplifting narratives, and stress relief. Safe for most emotional states.</p>
        </div>
        <div class='category-card card-intense'>
            <div class='card-title'>Intense</div>
            <p class='card-desc'>High tension and emotional investment. Gripping but potentially exhausting.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='category-card card-balanced'>
            <div class='card-title'>Balanced</div>
            <p class='card-desc'>Mixed emotional tones. Emotionally engaging but manageable for most viewers.</p>
        </div>
        <div class='category-card card-heavy'>
            <div class='card-title'>Heavy</div>
            <p class='card-desc'>Dark themes and heavy emotional toll. May not be suitable when feeling vulnerable.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#161b27; border:1px solid #2a2f3e; border-radius:10px; padding:16px 20px;'>
        <p style='color:#8892a4; font-size:0.82rem; margin:0;'>
        Use the <strong style='color:#b0b8cc'>sidebar</strong> to search for a specific show, browse all classifications, or learn more about how the model works.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── ANALYZE SHOW ─────────────────────────────────────────────────────────────
elif page == "Analyse Show":
    st.markdown("<h1>Analyse a Show</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2a2f3e; margin: 16px 0 28px 0'>", unsafe_allow_html=True)

    show_list = sorted(shows_df['title'].tolist())
    selected_show = st.selectbox("Select a TV show:", show_list)

    if st.button("Analyse This Show", type="primary"):
        show_data = shows_df[shows_df['title'] == selected_show].iloc[0]
        category = show_data['mood_category']
        color = category_colors.get(category, '#ffffff')
        desc = category_descriptions.get(category, '')

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='show-title'>{selected_show}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='mood-badge badge-{category}'>{category}</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background:#161b27; border-left:4px solid {color}; border-radius:0 10px 10px 0;
                    padding:16px 20px; margin-bottom:24px;'>
            <p style='color:#b0b8cc; font-size:0.9rem; margin:0;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Reviews Analysed", f"{int(show_data['review_count']):,}")
        with col2:
            sentiment = show_data['avg_sentiment']
            st.metric("Avg Sentiment Score", f"{sentiment:.2f}")
        with col3:
            st.metric("Classification", category)

        st.markdown("<br>", unsafe_allow_html=True)

        # Sentiment bar
        sent_val = float(show_data['avg_sentiment'])
        sent_pct = int((sent_val + 1) / 2 * 100)
        st.markdown("<h3>Sentiment Profile</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='margin: 12px 0 24px 0;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:6px;'>
                <span style='font-size:0.8rem; color:#8892a4;'>Negative</span>
                <span style='font-size:0.8rem; color:#8892a4;'>Positive</span>
            </div>
            <div style='background:#2a2f3e; border-radius:4px; height:8px; overflow:hidden;'>
                <div style='width:{sent_pct}%; height:100%; background:{color}; border-radius:4px; transition:width 0.5s;'></div>
            </div>
            <div style='text-align:center; margin-top:6px;'>
                <span style='font-size:0.8rem; color:#8892a4;'>Score: {sent_val:.3f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Viewer Reviews</h3>", unsafe_allow_html=True)
        import ast
        try:
            reviews = ast.literal_eval(show_data['sample_reviews'])
        except:
            reviews = [show_data['sample_reviews']]

        for i, review in enumerate(reviews[:3], 1):
            with st.expander(f"Review {i}"):
                st.write(review[:500] + "..." if len(str(review)) > 500 else review)

# ── ALL SHOWS ─────────────────────────────────────────────────────────────────
elif page == "All Shows":
    st.markdown("<h1>All Shows</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2a2f3e; margin: 16px 0 28px 0'>", unsafe_allow_html=True)

    category_counts = shows_df['mood_category'].value_counts()

    fig = go.Figure(data=[
        go.Bar(
            x=category_counts.index.tolist(),
            y=category_counts.values.tolist(),
            marker_color=[category_colors.get(c, '#888') for c in category_counts.index],
            marker_line_width=0,
        )
    ])
    fig.update_layout(
        plot_bgcolor='#161b27',
        paper_bgcolor='#161b27',
        font=dict(family='DM Sans', color='#8892a4', size=12),
        xaxis=dict(gridcolor='#2a2f3e', showline=False, tickfont=dict(color='#b0b8cc')),
        yaxis=dict(gridcolor='#2a2f3e', showline=False, tickfont=dict(color='#b0b8cc')),
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr style='border-color:#2a2f3e; margin: 8px 0 24px 0'>", unsafe_allow_html=True)

    for category in ['Positive', 'Balanced', 'Intense', 'Heavy']:
        shows_in_cat = shows_df[shows_df['mood_category'] == category]
        if len(shows_in_cat) > 0:
            color = category_colors[category]
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:14px;'>
                <div style='width:4px; height:20px; background:{color}; border-radius:2px;'></div>
                <span style='font-family:DM Serif Display, serif; font-size:1.1rem; color:#ffffff;'>{category}</span>
                <span style='font-size:0.8rem; color:#8892a4; margin-left:4px;'>{len(shows_in_cat)} shows</span>
            </div>
            """, unsafe_allow_html=True)

            for _, show in shows_in_cat.iterrows():
                st.markdown(f"""
                <div class='show-row'>
                    <span class='show-row-title'>{show['title']}</span>
                    <span class='show-row-meta'>{int(show['review_count'])} reviews &nbsp;&bull;&nbsp; sentiment {show['avg_sentiment']:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

# ── WHY IT MATTERS ───────────────────────────────────────────────────────────
elif page == "Why It Matters":
    st.markdown("<h1>Why It Matters</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2a2f3e; margin: 16px 0 28px 0'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-panel' style='margin-bottom: 20px;'>
        <p style='font-family: DM Serif Display, serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 14px;'>
        The relationship between television and mental health
        </p>
        <p>
        Television has become one of the most significant leisure activities of the modern age, with millions
        of people turning to streaming platforms daily. Research consistently shows that what we watch has a
        measurable impact on our mood, stress levels, and overall mental wellbeing. According to Adam (2023),
        watching TV shows can reduce stress and anxiety levels and increase feelings of happiness and
        relaxation but critically, this effect depends heavily on the type of content consumed.
        Not all television affects viewers equally.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-panel' style='margin-bottom: 20px;'>
        <p style='font-family: DM Serif Display, serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 14px;'>
        The gap in existing systems
        </p>
        <p>
        Current content classification systems age ratings, content advisories, genre labels were designed
        to protect younger audiences from inappropriate material. They were never designed to communicate the
        emotional weight of a programme for adult viewers managing their mental health. A show rated 18+
        could be darkly comic, deeply traumatic, or grippingly tense existing labels make no distinction
        between these very different experiences.
        </p>
        <p style='margin-top: 12px;'>
        ShunSpirit (2024) notes that TV shows have a unique ability to tap into our emotions through narrative,
        character development, and audiovisual effects. Many viewers form strong parasocial connections with
        characters and find their emotions are heavily impacted by the events that unfold on screen. For
        someone already experiencing anxiety or low mood, stumbling into the wrong show at the wrong time
        can have a genuinely negative effect on their mental state.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-panel' style='margin-bottom: 20px;'>
        <p style='font-family: DM Serif Display, serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 14px;'>
        A growing concern
        </p>
        <p>
        A 2024 study by the USC Norman Lear Center found that accurate and nuanced portrayals of mental health
        in entertainment can reduce stigma and encourage help-seeking behaviour demonstrating that the
        entertainment industry is increasingly aware of its responsibility towards viewer wellbeing.
        Meanwhile research by Starosta et al. (2021) found that individuals experiencing anxiety are more
        likely to binge-watch as a coping mechanism, sometimes making their anxiety worse in the process.
        The content they choose during those vulnerable moments matters more than ever.
        </p>
        <p style='margin-top: 12px;'>
        This project was built in response to that gap a practical tool that helps viewers make more
        mindful, informed choices about what they watch, based not on entertainment quality but on
        emotional impact.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quote highlight
    st.markdown("""
    <div style='border-left: 4px solid #4ecdc4; padding: 16px 24px; margin: 24px 0; background: #0d2e2c; border-radius: 0 10px 10px 0;'>
        <p style='color: #e8e8e8; font-family: DM Serif Display, serif; font-size: 1.05rem; font-style: italic; margin: 0 0 8px 0;'>
        "Many people experience a strong connection with TV show characters and find that their emotions
        are heavily impacted by the events that unfold on the screen."
        </p>
        <p style='color: #8892a4; font-size: 0.8rem; margin: 0;'>ShunSpirit, 2024</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#161b27; border:1px solid #2a2f3e; border-radius:10px; padding:14px 20px; margin-top: 8px;'>
        <p style='color:#4a5568; font-size:0.8rem; margin:0;'>
        References: Adam (2023) The Display Blog — ShunSpirit (2024) shunspirit.com — USC Norman Lear Center (2024) — Starosta et al. (2021) Frontiers in Psychiatry
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── ABOUT MODEL ──────────────────────────────────────────────────────────────
elif page == "About Model":
    st.markdown("<h1>About the Model</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2a2f3e; margin: 16px 0 28px 0'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Accuracy", "77%")
    with col2:
        st.metric("Model Type", "Random Forest")
    with col3:
        st.metric("Features Per Review", "115")

    st.markdown("<br>", unsafe_allow_html=True)

    # Accuracy by category
    st.markdown("<h3>Precision by Category</h3>", unsafe_allow_html=True)
    cats = ['Positive', 'Balanced', 'Intense', 'Heavy']
    precisions = [97, 70, 65, 68]
    colors_list = [category_colors[c] for c in cats]

    fig2 = go.Figure(data=[
        go.Bar(
            x=cats,
            y=precisions,
            marker_color=colors_list,
            marker_line_width=0,
            text=[f"{p}%" for p in precisions],
            textposition='outside',
            textfont=dict(color='#b0b8cc', size=13)
        )
    ])
    fig2.update_layout(
        plot_bgcolor='#161b27',
        paper_bgcolor='#161b27',
        font=dict(family='DM Sans', color='#8892a4', size=12),
        xaxis=dict(gridcolor='#2a2f3e', showline=False, tickfont=dict(color='#b0b8cc', size=13)),
        yaxis=dict(gridcolor='#2a2f3e', showline=False, tickfont=dict(color='#b0b8cc'), range=[0, 110]),
        margin=dict(l=20, r=20, t=30, b=20),
        height=300,
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<h3>Key Finding</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#161b27; border:1px solid #2a2f3e; border-radius:12px; padding:24px 28px; margin-bottom:20px;'>
        <div style='font-family:DM Serif Display,serif; font-size:2.4rem; color:#4ecdc4; line-height:1;'>+33 pts</div>
        <div style='color:#8892a4; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em; margin-top:4px;'>Accuracy improvement from TF-IDF features</div>
        <p style='color:#b0b8cc; font-size:0.88rem; margin-top:12px; line-height:1.7;'>
        Removing TF-IDF and relying solely on VADER sentiment scores and emotion features reduced
        accuracy from 77% to approximately 44%. The specific vocabulary viewers use in their reviews
        carries far more predictive signal than sentiment polarity alone.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3>Technical Details</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='info-panel'>
            <p><strong style='color:#e8e8e8; display:block; margin-bottom:10px;'>Features Extracted</strong>
            VADER sentiment scores (compound, positive, negative, neutral)<br>
            text2emotion dimensions (happy, sad, angry, fear, surprise)<br>
            Mental health keyword counts<br>
            Review length and punctuation intensity<br>
            TF-IDF term frequency weights
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='info-panel'>
            <p><strong style='color:#e8e8e8; display:block; margin-bottom:10px;'>Training Setup</strong>
            8,385 reviews across 50 TV shows<br>
            80/20 train-test split<br>
            200 decision trees, max depth 20<br>
            StandardScaler feature normalisation<br>
            Manual override system for edge cases
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#161b27; border:1px solid #2a2f3e; border-radius:10px; padding:14px 20px;'>
        <p style='color:#4a5568; font-size:0.8rem; margin:0;'>
        This tool is for informational purposes only. Individual emotional responses to media vary considerably.
        </p>
    </div>
    """, unsafe_allow_html=True)
