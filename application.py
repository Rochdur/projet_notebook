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

# 2. THÈME CLAIR 
st.markdown("""
<style>
/* Fond global */
.stApp { background-color: #FFFFFF; }

/* Sidebar : Fond gris clair et gestion de la largeur */
section[data-testid="stSidebar"] { 
    background-color: #F8F9FA !important; 
    border-right: 1px solid #DDD;
}

/* FIX DÉBORDEMENT TITRE SIDEBAR */
section[data-testid="stSidebar"] h1 {
    font-size: 24px !important; /* Taille réduite pour tenir sur une ligne */
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #1E1E1E !important;
}

/* Texte général et étiquettes des filtres */
section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label {
    font-size: 16px !important; 
    color: #1E1E1E !important;
}

/* Titres principaux du dashboard */
h1 { font-size: 40px !important; color: #1E1E1E !important; font-weight: 800 !important; }
h2 { font-size: 30px !important; color: #1E1E1E !important; font-weight: 700 !important; }

/* FIX BOUTON TÉLÉCHARGEMENT (PAS DE DÉBORDEMENT) */
.stDownloadButton button {
    width: 100% !important;
    white-space: nowrap !important; /* Force le texte sur une seule ligne */
    font-size: 14px !important;     /* Ajusté pour la largeur sidebar */
    padding: 10px 5px !important;
    font-weight: bold !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
}

.stDownloadButton button p {
    font-size: 14px !important;
    margin: 0 !important;
}

/* Métriques (KPI) */
div[data-testid="stMetricValue"] > div {
    font-size: 42px !important; 
    font-weight: 800 !important;
    color: #000000 !important;
}
div[data-testid="stMetricLabel"] > div > p {
    font-size: 18px !important;
    color: #495057 !important;
}

/* Fix visibilité Slider */
div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"], div[data-baseweb="slider"] div {
    color: #1E1E1E !important;
}
</style>
""", unsafe_allow_html=True)

# Fonction pour les graphiques Plotly
def update_light_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=14, color="#1E1E1E"),
        xaxis=dict(gridcolor='#E5E5E5', tickfont=dict(size=12)),
        yaxis=dict(gridcolor='#E5E5E5', tickfont=dict(size=12)),
        legend=dict(font=dict(size=12))
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
    except Exception:
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
        
        # Application du filtre avant l'exportation
        df_filtered = df[
            (df["experience_level"].isin(exp_selected)) &
            (df["company_size"].isin(size_selected)) &
            (df["salary_in_usd"].between(salary_range[0], salary_range[1]))
        ]

        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger le rapport (CSV)",
            data=csv,
            file_name='ds_salaries_report.csv',
            mime='text/csv',
        )

    # 5. DASHBOARD PRINCIPAL
    st.title("📊 Data Science Salaries Dashboard")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Salaire Moyen", f"${int(df_filtered['salary_in_usd'].mean()):,}")
    c2.metric("Salaire Médian", f"${int(df_filtered['salary_in_usd'].median()):,}")
    c3.metric("Nombre de Postes", len(df_filtered))

    st.markdown("---")

    # --- AJOUT : SECTION STATISTIQUES GÉNÉRALES ---
    st.subheader("📌 Statistiques générales")
    st.write(df_filtered.describe())

    st.markdown("---")

    # --- AJOUT : EXPLORATION VISUELLE DES DONNÉES ---
    st.subheader("🖼️ Exploration visuelle des données")
    col_vis1, col_vis2 = st.columns(2)
    with col_vis1:
        # Histogramme de la distribution des salaires
        fig_hist = px.histogram(df_filtered, x="salary_in_usd", nbins=30, title="Distribution des salaires (USD)", 
                               color_discrete_sequence=['#636EFA'], template="plotly_white")
        st.plotly_chart(update_light_layout(fig_hist), use_container_width=True)
    with col_vis2:
        # Camembert de la répartition par taille d'entreprise
        fig_pie = px.pie(df_filtered, names='company_size', title="Répartition par taille d'entreprise",
                        color_discrete_sequence=px.colors.qualitative.Pastel, template="plotly_white")
        st.plotly_chart(update_light_layout(fig_pie), use_container_width=True)

    st.markdown("---")

    # --- AJOUT : ANALYSE DES TENDANCES DE SALAIRES (Catégories) ---
    st.subheader("📈 Analyse des tendances de salaires")
    # Menu déroulant pour choisir la catégorie d'analyse
    cat_option = st.selectbox("Choisir une catégorie pour voir le salaire moyen :", 
                             ['experience_level', 'employment_type', 'job_title', 'company_location'])
    
    mean_data = df_filtered.groupby(cat_option)["salary_in_usd"].mean().sort_values(ascending=False).reset_index()
    fig_tend = px.bar(mean_data, x=cat_option, y="salary_in_usd", color="salary_in_usd",
                     title=f"Salaire moyen par {cat_option}", color_continuous_scale="Viridis", template="plotly_white")
    st.plotly_chart(update_light_layout(fig_tend), use_container_width=True)

    st.markdown("---")

    # --- AJOUT : ÉVOLUTION DES SALAIRES (TOP 10 POSTES) ---
    st.subheader("⏳ Évolution des salaires (Top 10 postes courants)")
    # Calcul des 10 postes les plus fréquents
    top_10 = df_filtered['job_title'].value_counts().nlargest(10).index
    df_top10 = df_filtered[df_filtered['job_title'].isin(top_10)]
    
    # Calcul du salaire moyen par année pour ces postes
    evo_data = df_top10.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    
    fig_line = px.line(evo_data, x="work_year", y="salary_in_usd", color="job_title", markers=True,
                      title="Évolution du salaire moyen annuel (Top 10 métiers)", template="plotly_white")
    fig_line.update_xaxes(dtick=1)
    st.plotly_chart(update_light_layout(fig_line), use_container_width=True)

    st.markdown("---")

    # ANALYSE OVERPAY / UNDERPAY
    st.subheader("⚖️ Analyse des écarts de rémunération par pays à poste équivalent")
    col_sel1, _ = st.columns([1.5, 2])
    with col_sel1:
        job_titles = sorted(df_filtered["job_title"].unique())
        default_idx = job_titles.index("Data Engineer") if "Data Engineer" in job_titles else 0
        selected_job = st.selectbox("Sélectionnez un métier :", job_titles, index=default_idx)

    median_global_job = df_filtered[df_filtered["job_title"] == selected_job]["salary_in_usd"].median()
    pay_analysis = df_filtered[df_filtered["job_title"] == selected_job].groupby("company_location")["salary_in_usd"].mean().reset_index()
    pay_analysis["diff_percent"] = ((pay_analysis["salary_in_usd"] - median_global_job) / median_global_job) * 100
    pay_analysis = pay_analysis.sort_values("diff_percent", ascending=False)

    fig_pay = px.bar(pay_analysis, x="company_location", y="diff_percent", color="diff_percent",
                     color_continuous_scale="RdYlGn", labels={"diff_percent": "Écart vs Médiane (%)"},
                     template="plotly_white")
    fig_pay.add_hline(y=0, line_dash="dash", line_color="black")
    st.plotly_chart(update_light_layout(fig_pay), use_container_width=True)

    st.markdown("---")

    # TREEMAP
    st.subheader("🌲 Répartition de la Masse Salariale")
    fig_tree = px.treemap(df_filtered, path=['job_title'], values='salary_in_usd', color='salary_in_usd',
                          color_continuous_scale='Viridis', template="plotly_white")
    st.plotly_chart(update_light_layout(fig_tree), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Distribution en France")
        df_fr = df_filtered[df_filtered["company_location"] == "FR"]
        if not df_fr.empty:
            fig_fr = px.box(df_fr, x="experience_level", y="salary_in_usd", color="experience_level", template="plotly_white")
            st.plotly_chart(update_light_layout(fig_fr), use_container_width=True)
        else: st.info("Aucune donnée pour la France.")

    with col2:
        st.subheader("🌎 USA vs Reste du Monde")
        fig_us = px.violin(df_filtered, x="is_us", y="salary_in_usd", color="is_us", box=True, template="plotly_white")
        st.plotly_chart(update_light_layout(fig_us), use_container_width=True)

    st.markdown("---")

    # CORRÉLATIONS
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🔗 Corrélations")
        num_df = df_filtered.select_dtypes(include=np.number)
        if num_df.shape[1] > 1:
            plt.style.use('default') 
            fig_corr, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(num_df.corr(), annot=True, cmap="Blues", ax=ax, center=0)
            fig_corr.patch.set_facecolor('#FFFFFF')
            st.pyplot(fig_corr)

    with col4:
        st.subheader("🏢 Médiane par Expérience & Taille")
        median_data = df_filtered.groupby(["experience_level", "company_size"])["salary_in_usd"].median().reset_index()
        fig_med = px.bar(median_data, x="experience_level", y="salary_in_usd", color="company_size", barmode="group", template="plotly_white")
        st.plotly_chart(update_light_layout(fig_med), use_container_width=True)

else:
    st.error("Données non trouvées.")