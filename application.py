import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


# 1. CONFIGURATION GLOBALE

st.set_page_config(
    page_title="Data Science Salaries Dashboard Pro",
    layout="wide"
)


# 2. THÈME 

st.markdown("""
<style>
.stApp { background-color: #121212; }
section[data-testid="stSidebar"] { background-color: #1E1E1E !important; border-right: 1px solid #333; }

/* TOUS LES TEXTES ET LABELS EN BLANC */
h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }

/* FIX VISIBILITÉ SLIDER & WIDGETS */
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"], div[data-baseweb="slider"] div {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
div[data-testid="stThumbValue"] { color: #FFFFFF !important; }

/* --- FIX BOUTON EXPORT (TÉLÉCHARGER) --- */
/* On force le texte du bouton en noir car le fond du bouton est blanc/gris clair */
button[kind="primary"], button[kind="secondary"] {
    color: #121212 !important;
}
/* Pour s'assurer que le texte dans le bouton de téléchargement spécifique est visible */
.stDownloadButton button p {
    color: #121212 !important;
}

/* --- FIX CHIFFRES DES METRICS (KPI) --- */
div[data-testid="stMetric"] {
    background-color: #1E1E1E;
    border: 1px solid #444;
    border-radius: 10px;
    padding: 10px;
}

div[data-testid="stMetricValue"] > div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-testid="stMetricLabel"] > div > p {
    color: #FFFFFF !important;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

def update_white_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color="white"),
        xaxis=dict(gridcolor='#333', tickfont=dict(color='white')),
        yaxis=dict(gridcolor='#333', tickfont=dict(color='white')),
        legend=dict(font=dict(color="white")),
        coloraxis_colorbar=dict(tickfont=dict(color='white'))
    )
    return fig


# 3. CHARGEMENT DES DONNÉES

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ds_salaries.csv")
        exp_map = {'EN': 'Entry', 'MI': 'Mid', 'SE': 'Senior', 'EX': 'Executive'}
        size_map = {'S': 'Small', 'M': 'Medium', 'L': 'Large'}
        df["experience_level"] = df["experience_level"].map(exp_map)
        df["company_size"] = df["company_size"].map(size_map)
        df["is_us"] = df["company_location"].apply(lambda x: "USA" if x == "US" else "Rest of World")
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    
    # 4. SIDEBAR & EXPORT
    
    with st.sidebar:
        st.title("🔍 Filtres & Export")
        
        min_sal, max_sal = int(df["salary_in_usd"].min()), int(df["salary_in_usd"].max())
        salary_range = st.slider("Plage de Salaire (USD)", min_sal, max_sal, (min_sal, max_sal))
        
        exp_selected = st.multiselect("Niveau d'expérience", 
                                      df["experience_level"].unique(), default=df["experience_level"].unique())
        
        size_selected = st.multiselect("Taille d'entreprise", 
                                       df["company_size"].unique(), default=df["company_size"].unique())

        st.markdown("---")
        # Le bouton d'exportation avec le fix CSS
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger le rapport (CSV)",
            data=csv,
            file_name='ds_salaries_report.csv',
            mime='text/csv',
        )

    df_filtered = df[
        (df["experience_level"].isin(exp_selected)) &
        (df["company_size"].isin(size_selected)) &
        (df["salary_in_usd"].between(salary_range[0], salary_range[1]))
    ]

    
    # 5. DASHBOARD PRINCIPAL
    
    st.title("📊 Data Science Salaries Dashboard")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Salaire Moyen", f"${int(df_filtered['salary_in_usd'].mean()):,}")
    c2.metric("Salaire Médian", f"${int(df_filtered['salary_in_usd'].median()):,}")
    c3.metric("Nombre de Postes", len(df_filtered))

    st.markdown("---")

    st.subheader("🌲 Répartition de la Masse Salariale par Métier")
    fig_tree = px.treemap(df_filtered, path=['job_title'], values='salary_in_usd',
                          color='salary_in_usd', color_continuous_scale='RdBu',
                          template="plotly_dark")
    st.plotly_chart(update_white_layout(fig_tree), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Distribution en France")
        df_fr = df_filtered[df_filtered["company_location"] == "FR"]
        if not df_fr.empty:
            fig_fr = px.box(df_fr, x="experience_level", y="salary_in_usd", color="experience_level", template="plotly_dark")
            st.plotly_chart(update_white_layout(fig_fr), use_container_width=True)
        else: st.info("Aucune donnée pour la France.")

    with col2:
        st.subheader("🌎 Comparaison Salariale : USA vs Reste du Monde")
        fig_us = px.violin(df_filtered, x="is_us", y="salary_in_usd", color="is_us", box=True, template="plotly_dark")
        st.plotly_chart(update_white_layout(fig_us), use_container_width=True)

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🔗 Corrélations")
        num_df = df_filtered.select_dtypes(include=np.number)
        if num_df.shape[1] > 1:
            plt.style.use('dark_background')
            fig_corr, ax = plt.subplots()
            sns.heatmap(num_df.corr(), annot=True, cmap="RdBu", ax=ax, center=0)
            fig_corr.patch.set_facecolor('#121212')
            st.pyplot(fig_corr)

    with col4:
        st.subheader("🏢 Médiane par Expérience & Taille")
        median_data = df_filtered.groupby(["experience_level", "company_size"])["salary_in_usd"].median().reset_index()
        fig_med = px.bar(median_data, x="experience_level", y="salary_in_usd", color="company_size", barmode="group", template="plotly_dark")
        st.plotly_chart(update_white_layout(fig_med), use_container_width=True)

else:
    st.error("Fichier de données manquant ou vide.")