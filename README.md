# ⚡ EE Mühendisi Portfolyo Sitesi

> Streamlit ile geliştirilmiş, Streamlit Cloud üzerinde yayınlanan interaktif portfolyo.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📁 Dosya Yapısı

```
portfolyo/
├── streamlit_app.py        ← Ana uygulama
├── requirements.txt        ← Bağımlılıklar
├── .gitignore              ← Git filtreleri
├── README.md               ← Bu dosya
│
├── data/
│   ├── projects.json       ← Proje bilgileri
│   └── certificates.json  ← Sertifika bilgileri
│
└── assets/
    ├── cert_fpga_vhdl.png  ← Sertifika görselleri
    ├── cert_python_ibm.png
    └── ...
```

---

## 🚀 Yerel Geliştirme

```bash
# Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
streamlit run streamlit_app.py
```

---

## ☁️ Streamlit Cloud'a Deploy

1. Bu repoyu GitHub'a push et
2. [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Repository ve `streamlit_app.py` dosyasını seç
4. API anahtarlarını **Settings → Secrets** bölümüne ekle
5. **Deploy** butonuna bas

---

## 🔐 Secrets Yönetimi

Yerel geliştirme için `.streamlit/secrets.toml` oluştur:

```toml
[api_keys]
bist_api_key = "ANAHTARINIZ"
```

> ⚠️ Bu dosya `.gitignore` tarafından otomatik olarak hariç tutulmaktadır.

---

## ✏️ Özelleştirme

| Dosya | Değiştirilecek Alan |
|-------|-------------------|
| `streamlit_app.py` | Ad, soyad, iletişim bilgileri |
| `data/projects.json` | GitHub URL'leri, proje açıklamaları |
| `data/certificates.json` | Sertifika bilgileri, doğrulama URL'leri |
| `assets/` | Sertifika PNG/JPG görsellerini buraya ekle |

---

## 🛠️ Kullanılan Teknolojiler

- **Streamlit** — Web arayüzü
- **Plotly** — İnteraktif grafikler (Radar, vb.)
- **Pandas** — Veri işleme
- **GitHub** — Versiyon kontrolü & kaynak kod
- **Streamlit Cloud** — Ücretsiz hosting
