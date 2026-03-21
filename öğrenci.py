import streamlit as st
import os
import requests
from streamlit_lottie import st_lottie

# ==============================
# 1. SAYFA AYARLARI
# ==============================
st.set_page_config(
    page_title="Dormify | Ensar Vakfı",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sidebar'ı tamamen gizleyen CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        .stMain { margin-left: 0; }
    </style>
""", unsafe_allow_html=True)

# Lottie Animasyon Yükleme Fonksiyonu
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_home_json = load_lottieurl("https://lottie.host/f5b2c1e5-8c7a-4f9e-9b4e-5d3f2c1e8b9a/x9Y2K1vB8m.json")

# ==============================
# 2. SESSION STATE (DURUM YÖNETİMİ)
# ==============================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Ana Sayfa"

if 'duyurular' not in st.session_state:
    st.session_state.duyurular = [
        {"baslik": "Teknik Bakım Duyurusu", "icerik": "İnternet altyapı çalışmaları nedeniyle bu gece kısa süreli kesintiler yaşanabilir.", "etiket": "ACİL", "renk": "#ef4444"},
        {"baslik": "Bahar Şenliği Kayıtları", "icerik": "Etkinlik katılım listesi lobi alanındaki panoya asılmıştır.", "etiket": "YENİ", "renk": "#3b82f6"}
    ]

if 'yemek_menusu' not in st.session_state:
    st.session_state.yemek_menusu = "🍲 Bugünün Menüsü: Yayla Çorbası, Tavuk Sote, Pilav ve Meyve."

# CSS Yükle
if os.path.exists("style.css"):
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# 3. HEADER (LOGO VE SİSTEME GİRİŞ YAP BUTONU)
# ==============================
top_col1, top_col2, top_col3 = st.columns([1.5, 3, 1.2])

with top_col1:
    logo_path = "images/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.markdown('<h2 style="margin: 0; color: #1e293b; font-size: 26px; font-weight: 800;">DORMİFY</h2>', unsafe_allow_html=True)

with top_col3:
    # Sayfalar arası geçiş: "Yönetici" kelimesi silindi, yerine istediğin "Sisteme Giriş Yap" eklendi.
    if st.session_state.current_page == "Ana Sayfa":
        if st.button("Sisteme Giriş Yap →", key="nav_btn"):
            st.session_state.current_page = "Giris Secim Sayfasi"
            st.rerun()
    else:
        if st.button("← Ana Sayfa", key="nav_btn"):
            st.session_state.current_page = "Ana Sayfa"
            st.rerun()

# ==============================
# 4. İÇERİK GÖSTERİMİ
# ==============================

# --- DURUM 1: ANA SAYFA ---
if st.session_state.current_page == "Ana Sayfa":
    
    st.write("") 
    if lottie_home_json:
        st_lottie(lottie_home_json, height=350, speed=1, loop=True, key="main_home_anim")
    
    st.markdown("""
        <div style="text-align: center; margin-top: -20px; margin-bottom: 50px;">
            <h4 style="color:#3b82f6; font-weight:700; letter-spacing: 2px; margin-bottom: 10px;">HOŞ GELDİNİZ</h4>
            <h1 style="font-size: 3.5rem; font-weight:900; color:#1e293b; margin:0;">Dormify <span style="color:#3b82f6;">Portal</span></h1>
            <p style="font-size: 1.2rem; color:#475569; margin-top: 15px;">
                Beylikdüzü Özel Ensar Vakfı Kız Yurdu <br>
                <b>Dijital Yönetim Platformu</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    stats = [("🌡️ ODA SICAKLIĞI", "22°C", "#3b82f6"), ("🍴 AKŞAM YEMEĞİ", "18:00", "#10b981"), ("📢 YENİ DUYURU", f"{len(st.session_state.duyurular)} Adet", "#f59e0b")]
    for col, (t, v, color) in zip([c1, c2, c3], stats):
        col.markdown(f'<div class="stat-box"><small>{t}</small><h2 style="color:{color}; font-size:2.5rem; font-weight:800; margin:0;">{v}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2.5, 1], gap="large")
    with col_main:
        st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">📢 Güncel Bilgilendirmeler</h3>', unsafe_allow_html=True)
        for d in st.session_state.duyurular:
            st.markdown(f"""
                <div class="custom-card" style="border-left: 8px solid {d['renk']};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="margin:0; font-weight:700;">{d['baslik']}</h4>
                        <span class="badge-new" style="background:{d['renk']}; color:white; padding:4px 12px; border-radius:20px; font-size:11px;">{d['etiket']}</span>
                    </div>
                    <p style="color:#475569; margin-top:10px;">{d['icerik']}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_side:
        st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">🛠️ Hızlı Erişim</h3>', unsafe_allow_html=True)
        st.button("🎫 İzin Formu Oluştur", use_container_width=True)
        st.button("🔧 Arıza Bildirimi", use_container_width=True)
        

# --- DURUM 2: ARKADAŞININ GİRİŞ SEÇİM EKRANI (HTML MANTIKLI) ---
elif st.session_state.current_page == "Giris Secim Sayfasi":
    # Arkadaşının animasyonlu mavi gradyan stilini buraya özel uyguluyoruz
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 25%, #bfdbfe 50%, #93c5fd 75%, #60a5fa 100%) !important;
        }
        </style>
        <div style="text-align: center; padding-top: 50px;">
            <h1 style="color: #1e293b; font-weight: 800; font-size: 3rem;">Hoş Geldiniz</h1>
            <p style="color: #475569; font-size: 1.2rem;">Lütfen sisteme giriş yapacağınız yetkiyi seçin</p>
        </div>
    """, unsafe_allow_html=True)

    col_empty1, col_selection, col_empty2 = st.columns([1, 1.2, 1])

    with col_selection:
        st.markdown('<div class="custom-card" style="text-align: center; margin-top: 30px;">', unsafe_allow_html=True)
        st.write("### Giriş Türü Belirleyin")
        st.write("")
        if st.button("👨‍🎓 ÖĞRENCİ OLARAK GİRİŞ", use_container_width=True):
            st.session_state.current_page = "Öğrenci Paneli" # Henüz kodlanmadıysa Ana Sayfa'ya atabilir
            st.rerun()
        st.write("")
        if st.button("🛡️ PERSONEL OLARAK GİRİŞ", use_container_width=True):
            st.session_state.current_page = "Yönetici Paneli"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- DURUM 3: YÖNETİCİ PANELİ ---
elif st.session_state.current_page == "Yönetici Paneli":
    st.markdown("<h2 style='text-align: center; color: #1e293b;'>⚙️ Yönetici Kontrol Paneli</h2>", unsafe_allow_html=True)
    
    col_adm1, col_adm2 = st.columns(2, gap="large")
    with col_adm1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📢 Yeni Duyuru Yayınla")
        y_baslik = st.text_input("Duyuru Başlığı")
        y_icerik = st.text_area("İçerik")
        if st.button("Duyuruyu Paylaş"):
             st.session_state.duyurular.insert(0, {"baslik": y_baslik, "icerik": y_icerik, "etiket": "YENİ", "renk": "#3b82f6"})
             st.success("Duyuru yayınlandı!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_adm2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🍴 Yemek Menüsü")
        st.info(st.session_state.yemek_menusu)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<center><p style='color:#94a3b8; padding:60px; font-size:12px;'>© 2026 Dormify | Ensar Vakfı</p></center>", unsafe_allow_html=True)