"""
Elektrik-Elektronik Mühendisi Portfolyo Sitesi
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
    page_title="Adınız | EE Mühendisi",
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
        <div class="skill-label">{label}</div>
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
NAV = ["🏠 Hakkımda", "🚀 Projelerim", "🏆 Sertifikalar", "📬 İletişim"]

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

    # Hero – profil fotoğrafı (st.image ile güvenli yöntem)
    profile_found = False
    profile_path = None
    for fname in ["profile.jpg", "profile.jpeg", "profile.png"]:
        p = BASE / "assets" / fname
        if p.exists():
            profile_found = True
            profile_path = str(p)
            break

    st.markdown("""
        <div class="hero-tag" style="margin-top:2rem;">// Elektrik-Elektronik Mühendisi</div>
        <h1 class="hero-name">Enes <span>BOZ</span></h1>
        <p class="hero-subtitle">
            FPGA Tasarım · Gömülü Sistemler · Python Geliştirme · Borsa Analiz Araçları
        </p>
        <div class="hero-badges">
            <span class="badge badge-cyan">VHDL / Vivado</span>
            <span class="badge badge-green">Python / Streamlit</span>
            <span class="badge badge-amber">Borsa Analizi</span>
            <span class="badge badge-cyan">STM32</span>
            <span class="badge badge-green">Web & Mobil</span>
        </div>
        <br>
    """, unsafe_allow_html=True)

    if profile_found:
        # Ortada yuvarlak görünen profil için CSS trick
        col_l, col_m, col_r = st.columns([2, 1, 2])
        with col_m:
            st.markdown("""
            <style>
            [data-testid="stImage"] img {
                border-radius: 50% !important;
                border: 3px solid rgba(0,212,255,0.5) !important;
                box-shadow: 0 0 30px rgba(0,212,255,0.25) !important;
                object-fit: cover !important;
                aspect-ratio: 1/1 !important;
            }
            </style>""", unsafe_allow_html=True)
            st.image(profile_path, use_container_width=True)
    else:
        col_l, col_m, col_r = st.columns([2, 1, 2])
        with col_m:
            st.markdown("""
            <div style="width:100%;aspect-ratio:1/1;border-radius:50%;
                        border:2px dashed rgba(0,212,255,0.3);
                        display:flex;align-items:center;justify-content:center;
                        background:#141c2e;flex-direction:column;gap:0.3rem;">
                <span style="font-size:2.5rem;">&#128100;</span>
                <span style="font-family:'Space Mono';font-size:0.55rem;
                             color:#3a4a66;text-align:center;">assets/profile.jpg</span>
            </div>""", unsafe_allow_html=True)

    # Hakkımda özet
    col1, _ = st.columns([3, 1], gap="large")
    with col1:
        st.markdown('<div class="section-header">Hakkımda<small>// ABOUT ME</small></div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#9aa3b8;line-height:1.8;font-size:0.95rem;">
        Genç yaşlardan itibaren farklı sektörlerde deneyim kazanarak çok yönlü bir bakış açısı
        geliştirmiş, sorumluluk almaktan çekinmeyen ve proaktif yaklaşımı benimsemiş bir
        profesyonelim. Güçlü liderlik özelliklerim ve ekip çalışmasına yatkınlığım sayesinde
        projelerde sonuç odaklı hareket eder, her görevde sürekli gelişimi ve yüksek kaliteyi hedeflerim.
        </p>
        <p style="color:#9aa3b8;line-height:1.8;font-size:0.95rem;margin-top:0.75rem;">
        Keskin gözlem yeteneğim ve analitik düşünme becerimle, karmaşık problemlere yenilikçi
        çözümler üretmekten heyecan duyarım. Mühendislik disiplinimin yanı sıra finans, ekonomi
        ve girişimcilik alanlarına duyduğum derin ilgiyle, bu alanlardaki bilgi birikimimi sürekli
        genişleterek <strong style="color:#00d4ff">disiplinler arası bir yetkinlik</strong> sunmayı amaçlıyorum.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <a href="https://enesboz-9.github.io/blog/" target="_blank"
           style="display:inline-flex;align-items:center;gap:0.5rem;
                  margin-top:1.25rem;padding:0.55rem 1.2rem;
                  background:linear-gradient(135deg,rgba(0,212,255,0.12),rgba(0,255,136,0.08));
                  border:1px solid rgba(0,212,255,0.4);border-radius:4px;
                  font-family:'Space Mono',monospace;font-size:0.8rem;
                  color:#00d4ff;text-decoration:none;
                  transition:all 0.2s;">
            ✍️ Teknoloji &amp; Yazılım Blogum → enesboz-9.github.io/blog
        </a>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="font-size:1.1rem;margin-top:1.5rem;">Eğitim<small>// EDUCATION</small></div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:4px;
                    padding:1rem 1.25rem;display:flex;align-items:flex-start;gap:1rem;">
            <span style="font-size:1.6rem;">🎓</span>
            <div>
                <div style="font-family:'Syne';font-size:0.95rem;font-weight:600;color:var(--text-primary);">
                    Marmara Üniversitesi
                </div>
                <div style="font-size:0.82rem;color:#00d4ff;margin:0.2rem 0;">
                    Electrical and Electronics Engineering (English)
                </div>
                <div style="font-family:'Space Mono';font-size:0.72rem;color:var(--text-muted);">
                    3. Sınıf · Devam Ediyor
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)






# ═══════════════════════════════════════════
#  SAYFA: YETENEKler
# ═══════════════════════════════════════════
# Yetenekler bölümü kaldırıldı.

# ═══════════════════════════════════════════
#  SAYFA: PROJELERİM
# ═══════════════════════════════════════════
elif page == NAV[1]:
    projects = load_json("data/projects.json")

    st.markdown('<div class="section-header">Projelerim<small>// MY PROJECTS</small></div>',
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

        card_html = (
            '<div class="project-card">' +
            f'<div class="card-category">{proj["category"]}</div>' +
            f'<div class="card-title">{proj["title"]}</div>' +
            f'<div class="card-subtitle">{proj["subtitle"]}</div>' +
            f'<div class="card-desc">{proj["description"]}</div>' +
            f'<div class="tag-row">{tag_html}</div>' +
            hw_html +
            '</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

        # Buton satırı
        github_url = proj.get("github_url", "")
        demo_url   = proj.get("demo_url", "")

        if demo_url and github_url:
            b1, b2 = st.columns(2)
            with b1:
                st.link_button("🔗 Projeyi İncele", demo_url, use_container_width=True)
            with b2:
                st.link_button("🐙 GitHub'da Gör", github_url, use_container_width=True)
        elif demo_url:
            st.link_button("🔗 Projeyi İncele", demo_url, use_container_width=True)
        elif github_url:
            st.link_button("🐙 GitHub'da Gör", github_url, use_container_width=True)

    cols = st.columns(min(len(filtered), 3) if filtered else 1, gap="large")
    for i, proj in enumerate(filtered):
        with cols[i % 3]:
            render_project_card(proj)

    if not filtered:
        st.info("Bu kategoride proje bulunamadı.")


# ═══════════════════════════════════════════
#  SAYFA: SERTİFİKALAR
# ═══════════════════════════════════════════
elif page == NAV[2]:
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
                    Görsel yüklenemedi
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Placeholder – sertifika yoksa
    if not certs:
        st.info("data/certificates.json dosyasına sertifika bilgilerinizi ekleyin.")


# ═══════════════════════════════════════════
#  SAYFA: İLETİŞİM
# ═══════════════════════════════════════════
elif page == NAV[3]:
    st.markdown('<div class="section-header">İletişim<small>// CONTACT</small></div>',
                unsafe_allow_html=True)

    col1, _ = st.columns([2, 1], gap="large")
    with col1:
        contacts = [
            ("📧", "E-posta", "enesboz446@gmail.com", "mailto:enesboz446@gmail.com"),
            ("💼", "LinkedIn", "linkedin.com/in/enesboz-00e", "https://linkedin.com/in/enesboz-00e"),
            ("🐙", "GitHub",   "github.com/enesboz-9",    "https://github.com/enesboz-9"),
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
