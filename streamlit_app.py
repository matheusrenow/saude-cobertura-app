import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import glob, os
import re

# ==============================
# Config & CSS
# ==============================
st.set_page_config(page_title="Cobertura de Planos", page_icon="📊", layout="wide")

CUSTOM_CSS = """
<style>
main .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1280px; }
h1 span.badge {
  font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 999px;
  background: linear-gradient(90deg, #22d3ee, #3b82f6); color: white; margin-left: .5rem;
}
.kpi-card {
  border-radius: 16px; padding: 16px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
}
.kpi-label { font-size: .9rem; color: #9CA3AF; margin-bottom: .35rem; }
.kpi-value { font-size: 1.6rem; font-weight: 700; line-height: 1.2; }
html:has([data-theme="light"]) .kpi-card { background: #ffffff; border: 1px solid #e5e7eb; }
.footer {
  opacity: .8; font-size: .9rem; border-top: 1px dashed rgba(255,255,255,0.15);
  padding-top: .75rem; margin-top: 1.25rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================
# Helpers
# ==============================
def fmt_int(n):
    try: return f"{int(n):,}".replace(",", ".")
    except: return "-"

def fmt_pct(x, nd=2):
    try: return f"{x*100:,.{nd}f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return "-"

def plotly_tidy(fig, ylabel=None, xlabel=None, title=None):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
        title=dict(text=title or "", x=0.02, xanchor="left", y=0.95),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    if ylabel: fig.update_yaxes(title=ylabel, showgrid=True, gridcolor="rgba(150,150,150,0.2)")
    if xlabel: fig.update_xaxes(title=xlabel, showgrid=False)
    return fig

@st.cache_data(show_spinner=True)
def load_data(path_or_buffer):
    df = None
    for enc in ["utf-8", "latin1", "cp1252"]:
        try:
            df = pd.read_csv(path_or_buffer, sep=";", encoding=enc)
            break
        except Exception:
            df = None
    if df is None:
        st.error("Não consegui ler o CSV.")
        st.stop()

    for col in ["BENEF_ASSISTENCIA_MEDICA","BENEF_EXCLUS_ODONTOLOGICO","BENEF_TOTAL"]:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors="coerce")
    if "PERIODO" in df.columns:
        df["PERIODO"] = pd.to_numeric(df["PERIODO"], errors="coerce").astype("Int64")
    for col in ["NM_MUNICIPIO","SG_UF","SEXO","FAIXA_ETARIA","NM_RM"]:
        if col in df.columns: df[col] = df[col].astype(str).str.strip()

    # remove colunas inúteis
    df.drop(columns=[c for c in ["POPULACAO","TX_COBERT_ASSISTENCIA_MEDICA",
                                 "TX_COBERT_EXCLUSIVAMENTE_ODONTOLOGICO","TX_COBERT_TOTAL"]
                     if c in df.columns], inplace=True, errors="ignore")
    return df

def normalize_series(s: pd.Series) -> pd.Series:
    total = s.sum()
    if total and total > 0: return s / total
    return s.replace(s, np.nan)

# ==============================
# Header
# ==============================
st.markdown("# Cobertura de Planos <span class='badge'>v1.2</span>", unsafe_allow_html=True)
st.caption("Painel didático com **BENEF_* (contagens)**. Série temporal removida, faixa etária ordenada, municípios zerados eliminados.")

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.header("⚙️ Dados")
    uploaded = st.file_uploader("📂 Envie seu CSV (separador ';')", type=["csv"])
    if uploaded is not None: df = load_data(uploaded)
    else:
        csvs = sorted(glob.glob(os.path.join("data","*.csv")))
        if not csvs: st.error("Nenhum CSV encontrado em data/"); st.stop()
        df = load_data(csvs[0])

    st.success(f"Linhas carregadas: {fmt_int(len(df))}")

    st.header("🔎 Filtros")
    dff = df.copy()

    if "SG_UF" in dff:
        ufs = sorted(dff["SG_UF"].dropna().unique().tolist())
        uf_sel = st.multiselect("UF", ufs, default=ufs)
        if uf_sel: dff = dff[dff["SG_UF"].isin(uf_sel)]
    if "SEXO" in dff:
        sexo_opts = sorted(dff["SEXO"].dropna().unique().tolist())
        sexo_sel = st.multiselect("Sexo", sexo_opts, default=sexo_opts)
        if sexo_sel: dff = dff[dff["SEXO"].isin(sexo_sel)]
    if "FAIXA_ETARIA" in dff:
        faixa_opts = sorted(dff["FAIXA_ETARIA"].dropna().unique().tolist())
        faixa_sel = st.multiselect("Faixa etária", faixa_opts, default=faixa_opts)
        if faixa_sel: dff = dff[dff["FAIXA_ETARIA"].isin(faixa_sel)]

    # ----- Remover municípios zerados globalmente -----
    metricas = [c for c in ["BENEF_TOTAL","BENEF_ASSISTENCIA_MEDICA","BENEF_EXCLUS_ODONTOLOGICO"] if c in dff.columns]
    if "NM_MUNICIPIO" in dff.columns and metricas:
        tmp = dff.copy()
        tmp["__MUN_NORM__"] = tmp["NM_MUNICIPIO"].astype(str).str.strip().str.lower()
        tmp[metricas] = tmp[metricas].fillna(0)
        agg = tmp.groupby("__MUN_NORM__")[metricas].sum()
        valid_norm = agg.sum(axis=1) > 0
        nomes_validos_norm = set(agg[valid_norm].index)
        dff = dff[dff["NM_MUNICIPIO"].astype(str).str.strip().str.lower().isin(nomes_validos_norm)]

    # Multiselect final de municípios
    if "NM_MUNICIPIO" in dff.columns:
        mun_opts = sorted(dff["NM_MUNICIPIO"].dropna().astype(str).str.strip().unique().tolist())
        mun_sel = st.multiselect("Município (opcional)", mun_opts)
        if mun_sel:
            dff = dff[dff["NM_MUNICIPIO"].isin(mun_sel)]

    st.divider()
    st.subheader("⚖️ Métrica base")
    metric_map = {
        "Beneficiários (TOTAL)":"BENEF_TOTAL",
        "Assistência Médica":"BENEF_ASSISTENCIA_MEDICA",
        "Exclusivo Odontológico":"BENEF_EXCLUS_ODONTOLOGICO",
    }
    metric_label = st.radio("O que analisar?", list(metric_map.keys()), index=0)
    metric_col = metric_map[metric_label]
    scale = st.radio("Escala", ["Contagem","% dentro do filtro"], index=0)

# ==============================
# KPIs
# ==============================
c1,c2,c3,c4 = st.columns(4)
benef_total = float(dff.get("BENEF_TOTAL",pd.Series(dtype=float)).sum())
benef_med   = float(dff.get("BENEF_ASSISTENCIA_MEDICA",pd.Series(dtype=float)).sum())
benef_odon  = float(dff.get("BENEF_EXCLUS_ODONTOLOGICO",pd.Series(dtype=float)).sum())
pct_med = (benef_med/benef_total) if (benef_total and benef_total>0) else np.nan
pct_odon= (benef_odon/benef_total) if (benef_total and benef_total>0) else np.nan

with c1: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Beneficiários (TOTAL)</div><div class='kpi-value'>{fmt_int(benef_total)}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Assistência Médica</div><div class='kpi-value'>{fmt_int(benef_med)}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Exclusivo Odontológico</div><div class='kpi-value'>{fmt_int(benef_odon)}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>% Médica / % Odonto</div><div class='kpi-value'>{fmt_pct(pct_med)} / {fmt_pct(pct_odon)}</div></div>", unsafe_allow_html=True)
st.divider()

# ==============================
# Abas (UF • Faixa etária • Municípios)
# ==============================
tab_uf, tab_faixa, tab_muni = st.tabs(["📍 Por UF","👥 Faixa Etária","🏙️ Municípios"])

with tab_uf:
    if {"SG_UF",metric_col}.issubset(dff.columns):
        by_uf = dff.groupby("SG_UF").agg(valor=(metric_col,"sum")).reset_index()
        if scale.startswith("%"):
            by_uf["valor_plot"] = normalize_series(by_uf["valor"])
            y_label,y_col,hover="% do total","valor_plot","%{y:.2%}"
        else:
            by_uf["valor_plot"]=by_uf["valor"]; y_label,y_col,hover="Beneficiários","valor_plot","%{y:,.0f}"
        fig1=px.bar(by_uf.sort_values(y_col,ascending=False),x="SG_UF",y=y_col)
        fig1=plotly_tidy(fig1,ylabel=y_label,xlabel="UF",title=f"{metric_label} por UF")
        fig1.update_traces(hovertemplate=f"UF=%{{x}}<br>{y_label}={hover}<extra></extra>")
        st.plotly_chart(fig1,use_container_width=True)

with tab_faixa:
    if {"FAIXA_ETARIA", metric_col}.issubset(dff.columns):
        by_fx = dff.groupby("FAIXA_ETARIA").agg(valor=(metric_col, "sum")).reset_index()
        by_fx = by_fx[~by_fx["FAIXA_ETARIA"].str.contains("Inconsistente", case=False, na=False)]

        # ordenação: "Até 1 ano" primeiro, depois pelas idades, "80 anos ou mais" por último
        def faixa_sort_key(faixa: str) -> float:
            s = faixa.strip().lower()
            if re.search(r"^até\s*1\s*ano", s): return -1.0
            if "80" in s and "mais" in s: return 80.0
            m = re.search(r"\d+", s)
            return float(m.group(0)) if m else 9999.0

        by_fx = by_fx.sort_values("FAIXA_ETARIA", key=lambda col: col.map(faixa_sort_key))

        if scale.startswith("%"):
            by_fx["valor_plot"] = normalize_series(by_fx["valor"])
            y_label,y_col,hover="% do total","valor_plot","%{y:.2%}"
        else:
            by_fx["valor_plot"] = by_fx["valor"]
            y_label,y_col,hover="Beneficiários","valor_plot","%{y:,.0f}"

        fig2 = px.bar(by_fx, x="FAIXA_ETARIA", y=y_col)
        fig2 = plotly_tidy(fig2, ylabel=y_label, xlabel="Faixa etária",
                           title=f"{metric_label} por faixa etária")
        fig2.update_xaxes(categoryorder="array", categoryarray=by_fx["FAIXA_ETARIA"])
        fig2.update_traces(hovertemplate=f"Faixa=%{{x}}<br>{y_label}={hover}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

with tab_muni:
    if {"NM_MUNICIPIO","PERIODO",metric_col}.issubset(dff.columns):
        ano_focus=int(dff["PERIODO"].dropna().max()) if "PERIODO" in dff and dff["PERIODO"].notna().any() else None
        muni_df=dff[dff["PERIODO"]==ano_focus] if ano_focus else dff.copy()
        muni_df=muni_df.groupby("NM_MUNICIPIO").agg(valor=(metric_col,"sum")).reset_index()
        muni_df = muni_df[muni_df["valor"] > 0]  # reforço: tira cidades zeradas
        if scale.startswith("%"):
            muni_df["valor_plot"]=normalize_series(muni_df["valor"])
            x_label,x_col,hover="% do total","valor_plot","%{x:.2%}"
        else:
            muni_df["valor_plot"]=muni_df["valor"]; x_label,x_col,hover="Beneficiários","valor_plot","%{x:,.0f}"
        top_n=muni_df.sort_values(x_col,ascending=False).head(20)
        fig3=px.bar(top_n,x=x_col,y="NM_MUNICIPIO",orientation="h")
        fig3=plotly_tidy(fig3,ylabel="Município",xlabel=x_label,
                         title=f"Top 20 municípios — {metric_label} ({ano_focus if ano_focus else 'geral'})")
        fig3.update_traces(hovertemplate=f"{x_label}={hover}<br>Município=%{{y}}<extra></extra>")
        st.plotly_chart(fig3,use_container_width=True)

# ==============================
# Tabela + Download
# ==============================
st.divider()
st.subheader("📄 Dados filtrados (amostra)")

metricas = [c for c in ["BENEF_TOTAL","BENEF_ASSISTENCIA_MEDICA","BENEF_EXCLUS_ODONTOLOGICO"] if c in dff.columns]
if "NM_MUNICIPIO" in dff.columns and metricas:
    tmp = dff.copy()
    tmp["__MUN_NORM__"] = tmp["NM_MUNICIPIO"].astype(str).str.strip().str.lower()
    tmp[metricas] = tmp[metricas].fillna(0)
    agg = tmp.groupby("__MUN_NORM__")[metricas].sum()
    valid_norm = agg.sum(axis=1) > 0
    nomes_validos_norm = set(agg[valid_norm].index)
    dff_table = dff[dff["NM_MUNICIPIO"].astype(str).str.strip().str.lower().isin(nomes_validos_norm)].copy()
else:
    dff_table = dff.copy()

show_cols=[c for c in ["PERIODO","SG_UF","NM_MUNICIPIO","SEXO","FAIXA_ETARIA",
                       "BENEF_TOTAL","BENEF_ASSISTENCIA_MEDICA","BENEF_EXCLUS_ODONTOLOGICO"]
           if c in dff_table.columns]
st.dataframe(dff_table[show_cols].head(1000))

@st.cache_data
def to_csv_bytes(df_in, cols):
    use=df_in[cols] if cols else df_in
    return use.to_csv(index=False,sep=";").encode("utf-8")

st.download_button("⬇️ Baixar CSV filtrado",data=to_csv_bytes(dff_table,show_cols),
                   file_name="dados_filtrados.csv",mime="text/csv")

st.markdown("<div class='footer'>Feito com ❤️ em Streamlit • v1.2</div>",unsafe_allow_html=True)
