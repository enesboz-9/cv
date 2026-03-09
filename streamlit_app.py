"""
Elektrik-Elektronik Mühendisi ENES boz  Portfolyo 
Streamlit Cloud üzerinde yayınlanmak üzere tasarlanmıştır.
"""

import streamlit as st
import json
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────
#  SAYFA AYARLARI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Enes BOZ | Elektrik Elektronik Mühendisi",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  TEMA & GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&family=Inter:wght@300;400;500&display=swap');

/* ── CSS Değişkenleri ── */
:root {
    --bg-primary:   #0a0e1a;
    --bg-secondary: #111827;
    --bg-card:      #141c2e;
    --accent-cyan:  #00d4ff;
    --accent-green: #00ff88;
    --accent-amber: #ffb703;
    --text-primary: #e8eaf0;
    --text-muted:   #6b7a99;
    --border:       rgba(0,212,255,0.15);
    --font-display: 'Syne', sans-serif;
    --font-mono:    'Space Mono', monospace;
    --font-body:    'Inter', sans-serif;
}

/* ── Genel arkaplan ── */
.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,212,255,0.08), transparent),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 80px,
            rgba(0,212,255,0.02) 80px,
            rgba(0,212,255,0.02) 81px
        );
    font-family: var(--font-body);
}

/* Streamlit varsayılan boşlukları sıfırla */
.block-container { padding-top: 2rem !important; max-width: 1200px !important; }
header, footer { visibility: hidden; }

/* ── Başlık kutusu ── */
.hero-wrapper {
    position: relative;
    padding: 4rem 2rem 3rem;
    text-align: center;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
}
.hero-tag {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--accent-cyan);
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-name {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1.05;
    margin: 0;
}
.hero-name span {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-family: var(--font-body);
    font-size: 1.1rem;
    color: var(--text-muted);
    margin-top: 1rem;
    font-weight: 300;
    letter-spacing: 0.05em;
}
.hero-badges {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}
.badge {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 0.35rem 0.85rem;
    border-radius: 2px;
    border: 1px solid;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-cyan  { color: var(--accent-cyan);  border-color: rgba(0,212,255,0.4);  background: rgba(0,212,255,0.06); }
.badge-green { color: var(--accent-green); border-color: rgba(0,255,136,0.4);  background: rgba(0,255,136,0.06); }
.badge-amber { color: var(--accent-amber); border-color: rgba(255,183,3,0.4);  background: rgba(255,183,3,0.06);  }

/* ── Bölüm başlıkları ── */
.section-header {
    font-family: var(--font-display);
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text-primary);
    border-left: 3px solid var(--accent-cyan);
    padding-left: 1rem;
    margin: 2.5rem 0 1.5rem;
}
.section-header small {
    display: block;
    font-size: 0.8rem;
    font-family: var(--font-mono);
    color: var(--text-muted);
    font-weight: 400;
    margin-top: 0.2rem;
    letter-spacing: 0.1em;
}

/* ── Proje kartları ── */
.project-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem;
    height: 100%;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.project-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
    opacity: 0;
    transition: opacity 0.2s;
}
.project-card:hover { border-color: rgba(0,212,255,0.4); transform: translateY(-2px); }
.project-card:hover::before { opacity: 1; }

.card-category {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.5rem;
}
.card-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}
.card-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
}
.card-desc {
    font-size: 0.85rem;
    color: #9aa3b8;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.75rem; }
.tag {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    padding: 0.2rem 0.55rem;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 2px;
    color: var(--accent-cyan);
}
.tag-green { background: rgba(0,255,136,0.08); border-color: rgba(0,255,136,0.2); color: var(--accent-green); }
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    margin-right: 0.4rem;
}
.status-active  { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.status-done    { background: var(--text-muted); }
.status-text { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted); }

/* ── Skill kartları ── */
.skill-block {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
}
.skill-label {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}
.skill-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    height: 4px;
    overflow: hidden;
}
.skill-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
}

/* ── Sertifika kartları ── */
.cert-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.cert-icon {
    font-size: 2rem;
    min-width: 2.5rem;
    text-align: center;
}
.cert-title { font-family: var(--font-display); font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }
.cert-issuer { font-size: 0.8rem; color: var(--text-muted); margin: 0.15rem 0; }
.cert-link { font-family: var(--font-mono); font-size: 0.7rem; color: var(--accent-cyan); text-decoration: none; }

/* ── İletişim kutusu ── */
.contact-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    text-align: center;
}
.contact-box a {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    color: var(--accent-cyan);
    text-decoration: none;
}
.contact-box a:hover { color: var(--accent-green); }

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.5rem 0;
}

/* Streamlit link butonlarını gizle */
.stLinkButton > a {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    background: transparent !important;
    border: 1px solid rgba(0,212,255,0.35) !important;
    color: var(--accent-cyan) !important;
    border-radius: 2px !important;
    padding: 0.3rem 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  YARDIMCI FONKSİYONLAR
# ─────────────────────────────────────────────
BASE = Path(__file__).parent

def load_json(path: str) -> list:
    full = BASE / path
    if full.exists():
        with open(full, encoding="utf-8") as f:
            return json.load(f)
    return []

def skill_bar(label: str, pct: int, color: str = "cyan"):
    gradient = (
        "linear-gradient(90deg,#00d4ff,#00ff88)" if color == "cyan"
        else "linear-gradient(90deg,#00ff88,#00d4ff)" if color == "green"
        else "linear-gradient(90deg,#ffb703,#ff6b35)"
    )
    st.markdown(f"""
    <div class="skill-block">
        <div class="skill-label">{label} <span style="float:right;color:#6b7a99">{pct}%</span></div>
        <div class="skill-bar-bg">
            <div class="skill-bar-fill" style="width:{pct}%;background:{gradient}"></div>
        </div>
    </div>""", unsafe_allow_html=True)

def status_html(s: str) -> str:
    cls = "status-active" if s in ("Aktif", "Aktif Geliştirme") else "status-done"
    return f'<span class="status-dot {cls}"></span><span class="status-text">{s}</span>'

CERT_ICONS = {
    "FPGA/Donanım": "🔲",
    "Python/Yazılım": "🐍",
    "Gömülü Sistemler": "💾",
}


# ─────────────────────────────────────────────
#  NAVİGASYON
# ─────────────────────────────────────────────
NAV = ["🏠 Hakkımda", "🛠️ Yetenekler", "🚀 Projeler", "🏆 Sertifikalar", "📬 İletişim"]

if "nav" not in st.session_state:
    st.session_state.nav = NAV[0]

cols_nav = st.columns(len(NAV))
for i, item in enumerate(NAV):
    with cols_nav[i]:
        if st.button(item, key=f"nav_{i}", use_container_width=True):
            st.session_state.nav = item

page = st.session_state.nav

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  SAYFA: HAKKIMDA
# ═══════════════════════════════════════════
if page == NAV[0]:

    # Hero
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-tag">// Elektrik-Elektronik Mühendisi</div>
        <h1 class="hero-name">Ad <span>Soyad</span></h1>
        <p class="hero-subtitle">
            FPGA Tasarım · Gömülü Sistemler · Python Geliştirme · Borsa Analiz Araçları
        </p>
        <div class="hero-badges">
            <span class="badge badge-cyan">VHDL / Vivado</span>
            <span class="badge badge-green">Python / Streamlit</span>
            <span class="badge badge-amber">Borsa Analizi</span>
            <span class="badge badge-cyan">RTL Tasarım</span>
            <span class="badge badge-green">Gömülü Linux</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hakkımda özet
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown('<div class="section-header">Hakkımda<small>// ABOUT ME</small></div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#9aa3b8;line-height:1.8;font-size:0.95rem;">
        Elektrik-Elektronik Mühendisliği alanında FPGA/VHDL donanım tasarımı ve Python tabanlı
        yazılım geliştirme konularında uzmanlaşmış bir mühendisim. Xilinx Vivado ekosisteminde
        RTL tasarım, sentez ve fiziksel implementasyon süreçlerinde deneyimliyim.
        </p>
        <p style="color:#9aa3b8;line-height:1.8;font-size:0.95rem;margin-top:0.75rem;">
        Yazılım tarafında ise Python ile veri odaklı uygulamalar ve özellikle
        <strong style="color:#00d4ff">BIST Analiz Terminali</strong> gibi fintech araçları
        geliştiriyorum. Streamlit ekosistemini kullanarak teknik analizleri interaktif
        web arayüzlerine dönüştürüyorum.
        </p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Hızlı Bakış<small>// QUICK STATS</small></div>',
                    unsafe_allow_html=True)

        stats = {
            "⚡ FPGA Projesi": "4+",
            "🐍 Python Projesi": "6+",
            "📐 VHDL Modülü": "10+",
            "🎓 Sertifika": "3",
        }
        for label, val in stats.items():
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.6rem 1rem;background:var(--bg-card);
                        border:1px solid var(--border);border-radius:4px;margin-bottom:0.5rem;">
                <span style="font-size:0.85rem;color:#9aa3b8;">{label}</span>
                <span style="font-family:'Space Mono',monospace;font-size:1.1rem;
                             color:#00d4ff;font-weight:700;">{val}</span>
            </div>""", unsafe_allow_html=True)

    # Radar grafik – uzmanlık alanları
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Uzmanlık Haritası<small>// EXPERTISE RADAR</small></div>',
                unsafe_allow_html=True)

    categories = ["VHDL/RTL", "FPGA Tasarım", "Python", "Veri Analizi",
                  "Gömülü Sistemler", "Borsa Analizi", "Streamlit/UI"]
    values     = [90, 85, 88, 80, 78, 82, 85]

    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(0,212,255,0.08)',
        line=dict(color='#00d4ff', width=2),
        marker=dict(color='#00ff88', size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor='rgba(255,255,255,0.06)', tickfont=dict(color='#6b7a99')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.06)',
                             tickfont=dict(color='#9aa3b8', size=12)),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════
#  SAYFA: YETENEKLER
# ═══════════════════════════════════════════
elif page == NAV[1]:
    st.markdown('<div class="section-header">Teknik Yetenekler<small>// TECHNICAL SKILLS</small></div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3, gap="large")

    with col_a:
        st.markdown("""
        <div style="font-family:'Space Mono';font-size:0.7rem;color:#00d4ff;
                    letter-spacing:0.2em;text-transform:uppercase;margin-bottom:1rem;">
            ⬡ FPGA / VHDL
        </div>""", unsafe_allow_html=True)
        skill_bar("VHDL-2008", 90, "cyan")
        skill_bar("Xilinx Vivado", 85, "cyan")
        skill_bar("ModelSim (Simülasyon)", 80, "cyan")
        skill_bar("RTL Tasarım / FSM", 88, "cyan")
        skill_bar("Timing Analiz (STA)", 72, "cyan")

    with col_b:
        st.markdown("""
        <div style="font-family:'Space Mono';font-size:0.7rem;color:#00ff88;
                    letter-spacing:0.2em;text-transform:uppercase;margin-bottom:1rem;">
            ⬡ Python / Yazılım
        </div>""", unsafe_allow_html=True)
        skill_bar("Python 3.x", 90, "green")
        skill_bar("Pandas / NumPy", 85, "green")
        skill_bar("Plotly / Matplotlib", 82, "green")
        skill_bar("Streamlit", 88, "green")
        skill_bar("REST API Entegrasyonu", 75, "green")

    with col_c:
        st.markdown("""
        <div style="font-family:'Space Mono';font-size:0.7rem;color:#ffb703;
                    letter-spacing:0.2em;text-transform:uppercase;margin-bottom:1rem;">
            ⬡ Borsa Analizi
        </div>""", unsafe_allow_html=True)
        skill_bar("Teknik Analiz", 80, "amber")
        skill_bar("RSI / MACD / BB", 78, "amber")
        skill_bar("BIST Veri API", 75, "amber")
        skill_bar("Backtest Geliştirme", 65, "amber")
        skill_bar("Veri Görselleştirme", 85, "amber")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Araçlar & Ortamlar
    st.markdown('<div class="section-header">Araçlar & Ortamlar<small>// TOOLS & ENVIRONMENTS</small></div>',
                unsafe_allow_html=True)

    tools = [
        ("⚙️", "Xilinx Vivado 2023.2", "FPGA sentez & implementasyon"),
        ("🔬", "ModelSim / QuestaSim", "VHDL davranışsal simülasyon"),
        ("🐍", "VS Code + Pylance", "Python geliştirme ortamı"),
        ("📊", "Jupyter Notebook", "Veri analiz & prototipleme"),
        ("🔧", "Git / GitHub", "Versiyon kontrolü"),
        ("☁️", "Streamlit Cloud", "Web uygulaması dağıtımı"),
        ("🐧", "Ubuntu / WSL2", "Geliştirme ortamı"),
        ("📐", "LTspice", "Analog devre simülasyonu"),
    ]
    rows = [tools[i:i+4] for i in range(0, len(tools), 4)]
    for row in rows:
        cols = st.columns(4, gap="medium")
        for j, (icon, name, desc) in enumerate(row):
            with cols[j]:
                st.markdown(f"""
                <div style="background:var(--bg-card);border:1px solid var(--border);
                            border-radius:4px;padding:1rem;text-align:center;margin-bottom:0.75rem;">
                    <div style="font-size:1.8rem;margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-family:'Syne';font-size:0.85rem;color:var(--text-primary);font-weight:600;">{name}</div>
                    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:0.2rem;">{desc}</div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
#  SAYFA: PROJELER
# ═══════════════════════════════════════════
elif page == NAV[2]:
    projects = load_json("data/projects.json")

    st.markdown('<div class="section-header">Proje Galerisi<small>// PROJECT GALLERY</small></div>',
                unsafe_allow_html=True)

    # Filtre
    all_cats = ["Tümü"] + sorted(set(p["category"] for p in projects))
    sel_cat = st.selectbox("Kategoriye göre filtrele", all_cats, index=0,
                           label_visibility="collapsed")

    filtered = projects if sel_cat == "Tümü" else [p for p in projects if p["category"] == sel_cat]

    # Öne çıkan projeler
    featured = [p for p in filtered if p.get("highlight")]
    others   = [p for p in filtered if not p.get("highlight")]

    def render_project_card(proj):
        tag_html = " ".join(f'<span class="tag">{t}</span>' for t in proj["tags"])
        hw_html  = ""
        if proj.get("hardware"):
            hw_items = " ".join(f'<span class="tag tag-green">{h}</span>' for h in proj["hardware"])
            hw_html  = f'<div style="margin-top:0.5rem;">{hw_items}</div>'
        status = status_html(proj.get("status", ""))

        st.markdown(f"""
        <div class="project-card">
            <div class="card-category">{proj["category"]}</div>
            <div class="card-title">{proj["title"]}</div>
            <div class="card-subtitle">{proj["subtitle"]}</div>
            <div class="card-desc">{proj["description"]}</div>
            <div class="tag-row">{tag_html}</div>
            {hw_html}
            <div style="margin-top:1rem;display:flex;align-items:center;justify-content:space-between;">
                {status}
            </div>
        </div>""", unsafe_allow_html=True)
        st.link_button("GitHub'da İncele →", proj["github_url"])

    if featured:
        st.markdown("**⭐ Öne Çıkan Projeler**")
        c1, c2 = st.columns(2, gap="large")
        for i, proj in enumerate(featured):
            with (c1 if i % 2 == 0 else c2):
                render_project_card(proj)

    if others:
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("**Diğer Projeler**")
        cols = st.columns(min(len(others), 3), gap="large")
        for i, proj in enumerate(others):
            with cols[i % 3]:
                render_project_card(proj)

    if not filtered:
        st.info("Bu kategoride proje bulunamadı.")


# ═══════════════════════════════════════════
#  SAYFA: SERTİFİKALAR
# ═══════════════════════════════════════════
elif page == NAV[3]:
    certs = load_json("data/certificates.json")

    st.markdown('<div class="section-header">Sertifikalar<small>// CERTIFICATIONS</small></div>',
                unsafe_allow_html=True)

    assets_dir = BASE / "assets"

    for cert in certs:
        icon = CERT_ICONS.get(cert.get("category", ""), "📄")
        img_path = assets_dir / cert.get("image_file", "")

        col_info, col_img = st.columns([3, 2], gap="large")
        with col_info:
            st.markdown(f"""
            <div class="cert-card">
                <div class="cert-icon">{icon}</div>
                <div>
                    <div class="cert-title">{cert['title']}</div>
                    <div class="cert-issuer">📌 {cert['issuer']} · {cert['date']}</div>
                    <div style="font-size:0.8rem;color:#9aa3b8;margin:0.4rem 0 0.5rem;">
                        {cert.get('description','')}
                    </div>
                    <a class="cert-link" href="{cert['credential_url']}" target="_blank">
                        🔗 Sertifikayı Doğrula →
                    </a>
                </div>
            </div>""", unsafe_allow_html=True)

        with col_img:
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            else:
                st.markdown(f"""
                <div style="background:var(--bg-card);border:1px dashed rgba(0,212,255,0.2);
                            border-radius:4px;padding:2rem;text-align:center;color:var(--text-muted);
                            font-family:'Space Mono';font-size:0.75rem;">
                    📁 {cert.get('image_file','')}<br>
                    <span style="font-size:0.65rem;">/assets klasörüne ekleyin</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Placeholder – sertifika yoksa
    if not certs:
        st.info("data/certificates.json dosyasına sertifika bilgilerinizi ekleyin.")


# ═══════════════════════════════════════════
#  SAYFA: İLETİŞİM
# ═══════════════════════════════════════════
elif page == NAV[4]:
    st.markdown('<div class="section-header">İletişim<small>// CONTACT</small></div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        contacts = [
            ("📧", "E-posta", "adsoyadiniz@gmail.com", "mailto:adsoyadiniz@gmail.com"),
            ("💼", "LinkedIn", "linkedin.com/in/kullanici-adiniz", "https://linkedin.com/in/kullanici-adiniz"),
            ("🐙", "GitHub",   "github.com/kullanici-adiniz",      "https://github.com/kullanici-adiniz"),
        ]
        for icon, label, display, url in contacts:
            st.markdown(f"""
            <div class="cert-card" style="margin-bottom:0.75rem;">
                <div class="cert-icon">{icon}</div>
                <div>
                    <div class="cert-title">{label}</div>
                    <a class="cert-link" href="{url}" target="_blank">{display}</a>
                </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="contact-box" style="margin-top:0;">
            <div style="font-family:'Syne';font-size:1rem;color:var(--text-primary);margin-bottom:0.5rem;">
                Açık Pozisyonlar
            </div>
            <div style="font-size:0.82rem;color:#9aa3b8;line-height:1.7;">
                ✅ FPGA / RTL Mühendisi<br>
                ✅ Gömülü Sistem Mühendisi<br>
                ✅ Python Geliştirici<br>
                ✅ Serbest / Freelance
            </div>
        </div>""", unsafe_allow_html=True)

    # GitHub & Secrets rehberi
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">GitHub & Streamlit Cloud Rehberi<small>// DEPLOYMENT GUIDE</small></div>',
                unsafe_allow_html=True)

    with st.expander("📁 .gitignore — Neleri commit etmemeli?", expanded=True):
        st.code("""# Streamlit gizli anahtarları (ASLA commit etme!)
.streamlit/secrets.toml

# Ortam değişkenleri
.env

# Python önbelleği
__pycache__/
*.pyc

# Sanal ortam
.venv/
venv/

# IDE dosyaları
.vscode/
.idea/

# OS dosyaları
.DS_Store
Thumbs.db
""", language="gitignore")

    with st.expander("🔐 Streamlit Cloud — Secrets Yönetimi"):
        st.markdown("""
**Streamlit Cloud'da API anahtarı veya şifre kullanmak için:**

1. `https://share.streamlit.io` → Uygulamanızı seçin → **Settings → Secrets**
2. Aşağıdaki formatta secret tanımlayın:

```toml
# .streamlit/secrets.toml (yerel geliştirme)
[api_keys]
bist_api_key = "BURAYA_ANAHTARINIZI_YAZIN"
github_token = "ghp_xxxxxxxxxxxx"
```

3. Kodunuzda erişim:
```python
import streamlit as st

api_key = st.secrets["api_keys"]["bist_api_key"]
```

> ⚠️ `secrets.toml` dosyasını hiçbir zaman GitHub'a push etmeyin.
> `.gitignore` dosyasına `.streamlit/secrets.toml` satırını eklediğinizden emin olun.
""")

    with st.expander("🚀 GitHub'a Yükleme Adımları"):
        st.markdown("""
```bash
# 1. Repo başlat
git init
git remote add origin https://github.com/KULLANICI/portfolyo.git

# 2. Dosyaları ekle (.gitignore otomatik filtreler)
git add .
git commit -m "feat: portfolyo ilk yükleme"
git push -u origin main

# 3. Streamlit Cloud'da yayına al
# → share.streamlit.io → New app
# → Repository: KULLANICI/portfolyo
# → Branch: main
# → Main file path: streamlit_app.py
# → Deploy!
```
""")


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;margin-top:3rem;
            border-top:1px solid rgba(0,212,255,0.1);">
    <span style="font-family:'Space Mono';font-size:0.7rem;color:#3a4a66;">
        ⚡ Built with Streamlit · Designed for Engineers · {year}
    </span>
</div>
""".replace("{year}", "2025"), unsafe_allow_html=True)
