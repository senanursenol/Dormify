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

# Sidebar'ı gizleyen ve kartları düzenleyen CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        .stMain { margin-left: 0; }
        .custom-card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
        }
        .stat-box {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* === YENİ MODERN GÜNÜN MENÜSÜ TASARIMI === */
        .modern-menu-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.4);
            margin-bottom: 20px;
            text-align: center;
        }
        .menu-items-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        .menu-item-pill {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            color: #166534;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .afiyet-text {
            color: #15803d;
            font-size: 0.75rem;
            font-weight: 800;
            margin-top: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

# Lottie Yükleme
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_home_json = load_lottieurl("https://lottie.host/f5b2c1e5-8c7a-4f9e-9b4e-5d3f2c1e8b9a/x9Y2K1vB8m.json")

# ==============================
# 2. SESSION STATE
# ==============================
if 'current_page' not in st.session_state: st.session_state.current_page = "Ana Sayfa"
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'admin_sub_page' not in st.session_state: st.session_state.admin_sub_page = "Seçim"

if 'duyurular' not in st.session_state:
    st.session_state.duyurular = [
        {"baslik": "Teknik Bakım Duyurusu", "icerik": "İnternet altyapı çalışmaları nedeniyle bu gece kısa süreli kesintiler yaşanabilir.", "etiket": "ACİL", "renk": "#ef4444"},
        {"baslik": "Bahar Şenliği Kayıtları", "icerik": "Etkinlik katılım listesi lobi alanındaki panoya asılmıştır.", "etiket": "YENİ", "renk": "#3b82f6"}
    ]

if 'yemek_menusu' not in st.session_state:
    st.session_state.yemek_menusu = "Yayla Çorbası, Tavuk Sote, Pilav, Meyve"

if 'ariza_listesi' not in st.session_state:
    st.session_state.ariza_listesi = [{"oda": "202", "aciklama": "Musluk bozuk", "tarih": "20.05.2024"}]

# CSS Dosyası Yükle
if os.path.exists("style.css"):
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# 3. HEADER
# ==============================
top_col1, top_col2, top_col3 = st.columns([1.5, 3, 1.2])

with top_col1:
    logo_path = "images/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.markdown('<h2 style="margin: 0; color: #1e293b; font-size: 26px; font-weight: 800;">DORMİFY</h2>', unsafe_allow_html=True)

with top_col3:
    if st.session_state.current_page == "Ana Sayfa":
        if st.button("Sisteme Giriş Yap →", key="nav_btn"):
            st.session_state.current_page = "Giris Secim Sayfasi"
            st.rerun()
    else:
        if st.button("← Ana Sayfa", key="nav_btn"):
            st.session_state.current_page = "Ana Sayfa"
            st.session_state.admin_sub_page = "Seçim"
            st.rerun()

# ==============================
# 4. İÇERİK
# ==============================

if st.session_state.current_page == "Ana Sayfa":
    if lottie_home_json: st_lottie(lottie_home_json, height=350, key="main_home_anim")
    
    st.markdown('<div style="text-align: center; margin-top: -20px; margin-bottom: 50px;"><h1 style="font-size: 3.5rem; font-weight:900; color:#1e293b; margin:0;">Dormify <span style="color:#3b82f6;">Portal</span></h1><p style="font-size: 1.2rem; color:#475569; margin-top: 15px;">Beylikdüzü Özel Ensar Vakfı Kız Yurdu <br><b>Dijital Yönetim Platformu</b></p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_main, col_side = st.columns([2.5, 1], gap="large")
    with col_main:
        st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">📢 Güncel Bilgilendirmeler</h3>', unsafe_allow_html=True)
        for d in st.session_state.duyurular:
            st.markdown(f'<div class="custom-card" style="border-left: 8px solid {d["renk"]};"><h4>{d["baslik"]}</h4><p>{d["icerik"]}</p></div>', unsafe_allow_html=True)
    
    with col_side:
        # === YENİ MODERN MENÜ KISMI ===
        st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">🍴 Bugün Ne Var?</h3>', unsafe_allow_html=True)
        
        # Yemekleri virgülle ayırıp frontend için ikon atayalım
        menu_items = st.session_state.yemek_menusu.split(', ')
        icons = ["🍲", "🍗", "🍚", "🍎"]
        
        # HTML Oluşturma
        pills_html = "".join([
            f'<div class="menu-item-pill">{icons[i] if i < len(icons) else "🍽️"} {item.strip()}</div>' 
            for i, item in enumerate(menu_items)
        ])
        
        st.markdown(f"""
            <div class="modern-menu-card">
                <div class="menu-items-container">
                    {pills_html}
                </div>
                <div class="afiyet-text">AFİYET OLSUN!</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.button("🎫 İzin Formu Oluştur", use_container_width=True, key="btn_izin")
        st.button("🔧 Arıza Bildirimi", use_container_width=True, key="btn_ariza")
        

elif st.session_state.current_page == "Giris Secim Sayfasi":
    _, col_sel, _ = st.columns([1, 1.2, 1])
    with col_sel:
        st.markdown('<div class="custom-card" style="text-align: center; margin-top: 30px;"><h2>Hoş Geldiniz</h2>', unsafe_allow_html=True)
        if st.button("👨‍🎓 ÖĞRENCİ OLARAK GİRİŞ", use_container_width=True): st.info("Yakında!")
        if st.button("🛡️ PERSONEL OLARAK GİRİŞ", use_container_width=True):
            st.session_state.current_page = "Yönetici Paneli"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "Yönetici Paneli":
    if not st.session_state.admin_logged_in:
        _, col_l2, _ = st.columns([1, 1, 1])
        with col_l2:
            st.markdown('<div class="custom-card" style="margin-top:50px;"><h3>🛡️ Giriş</h3>', unsafe_allow_html=True)
            u = st.text_input("Kullanıcı Adı")
            p = st.text_input("Şifre", type="password")
            if st.button("Giriş Yap", use_container_width=True):
                if u == "admin" and p == "ensar123":
                    st.session_state.admin_logged_in = True; st.rerun()
                else: st.error("Hatalı!")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.title("⚙️ Kontrol Paneli")
        if st.button("Çıkış 🚪"): st.session_state.admin_logged_in = False; st.rerun()
        st.divider()

        if st.session_state.admin_sub_page == "Seçim":
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown('<div class="custom-card" style="text-align:center;">📢 Duyuru</div>', unsafe_allow_html=True)
                if st.button("Duyuru Sayfasına Git", use_container_width=True): st.session_state.admin_sub_page = "Duyuru"; st.rerun()
            with sc2:
                st.markdown('<div class="custom-card" style="text-align:center;">🍴 Yemek</div>', unsafe_allow_html=True)
                if st.button("Yemek Sayfasına Git", use_container_width=True): st.session_state.admin_sub_page = "Yemek"; st.rerun()
            with sc3:
                st.markdown('<div class="custom-card" style="text-align:center;">🔧 Arıza</div>', unsafe_allow_html=True)
                if st.button("Arıza Sayfasına Git", use_container_width=True): st.session_state.admin_sub_page = "Ariza"; st.rerun()

        elif st.session_state.admin_sub_page == "Duyuru":
            if st.button("← Geri"): st.session_state.admin_sub_page = "Seçim"; st.rerun()
            st.markdown('<div class="custom-card"><h3>📢 Duyuru Yayınla</h3>', unsafe_allow_html=True)
            b = st.text_input("Başlık")
            i = st.text_area("İçerik")
            if st.button("Yayınla"):
                st.session_state.duyurular.insert(0, {"baslik": b, "icerik": i, "etiket": "YENİ", "renk": "#3b82f6"})
                st.success("Paylaşıldı!")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.admin_sub_page == "Yemek":
            if st.button("← Geri"): st.session_state.admin_sub_page = "Seçim"; st.rerun()
            st.markdown('<div class="custom-card"><h3>🍴 Yemek Güncelle</h3>', unsafe_allow_html=True)
            y = st.text_area("Menü (Yemekleri virgülle ayırın)", value=st.session_state.yemek_menusu)
            if st.button("Güncelle"): st.session_state.yemek_menusu = y; st.success("Tamam!")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.admin_sub_page == "Ariza":
            if st.button("← Geri"): st.session_state.admin_ekran = "Seçim"; st.rerun()
            st.markdown('<div class="custom-card"><h3>🔧 Bildirimler</h3>', unsafe_allow_html=True)
            for i, a in enumerate(st.session_state.ariza_listesi):
                st.write(f"🚪 Oda {a['oda']} - {a['aciklama']}")
                if st.button(f"Kapat #{i}"): st.session_state.ariza_listesi.pop(i); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<center><p style='color:#94a3b8; padding:60px; font-size:12px;'>© 2026 Dormify | Ensar Vakfı</p></center>", unsafe_allow_html=True)