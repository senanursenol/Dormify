import streamlit as st
import os

# Sayfa Ayarları
st.set_page_config(page_title="Dormify | Yönetici Paneli", page_icon="⚙️", layout="wide")

# CSS Yükle (Ana sayfadaki stilleri kullanabiliriz)
if os.path.exists("style.css"):
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# 1. ADMIN HEADER
# ==============================
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 30px; border-radius: 20px; color: white; margin-bottom: 30px;">
        <h1 style="margin:0;">⚙️ Yönetim Paneli</h1>
        <p style="margin:0; opacity:0.8;">Beylikdüzü Özel Ensar Vakfı Kız Yurdu Portal Yönetimi</p>
    </div>
""", unsafe_allow_html=True)

# ==============================
# 2. ÖZET BİLGİ KARTLARI (KÜÇÜK)
# ==============================
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="stat-box"><h5>Toplam Öğrenci</h5><h2>124</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-box"><h5>Aktif Duyuru</h5><h2>3</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-box"><h5>Bekleyen Talepler</h5><h2>5</h2></div>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# ==============================
# 3. YÖNETİM SEKMELERİ
# ==============================
tab_duyuru, tab_yemek, tab_izin = st.tabs(["📢 Duyuru Yönetimi", "🍴 Yemek Menüsü Güncelle", "🎫 İzin Onayları"])

with tab_duyuru:
    st.subheader("Yeni Duyuru Yayınla")
    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        d_baslik = st.text_input("Duyuru Başlığı", placeholder="Örn: Teknik Bakım Hakkında")
        d_icerik = st.text_area("Duyuru İçeriği", placeholder="Öğrencilere iletilecek mesajı buraya yazın...")
        d_oncelik = st.selectbox("Öncelik Seviyesi", ["Normal", "Önemli", "ACİL"])
        
        if st.button("🚀 Duyuruyu Yayınla", use_container_width=True):
            st.success(f"'{d_baslik}' başlıklı duyuru başarıyla yayına alındı!")
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

with tab_yemek:
    st.subheader("Günlük Yemek Listesi")
    col_y1, col_y2 = st.columns(2)
    
    with col_y1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 🌞 Öğle Yemeği")
        ogle_ana = st.text_input("Ana Yemek (Öğle)")
        ogle_yan = st.text_input("Yardımcı Yemek (Öğle)")
        ogle_ek = st.text_input("Ekstra (Öğle)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_y2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 🌙 Akşam Yemeği")
        aksam_ana = st.text_input("Ana Yemek (Akşam)")
        aksam_yan = st.text_input("Yardımcı Yemek (Akşam)")
        aksam_ek = st.text_input("Ekstra (Akşam)")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💾 Menüyü Güncelle", use_container_width=True):
        st.success("Yemek menüsü tüm öğrenciler için güncellendi!")

with tab_izin:
    st.subheader("Bekleyen İzin Talepleri")
    # Örnek bir tablo yapısı
    izin_data = [
        {"Öğrenci": "Manolya D.", "Oda": "204", "Tür": "Gece İzni", "Tarih": "21.03.2026"},
        {"Öğrenci": "Ayşe Y.", "Oda": "102", "Tür": "Haftasonu", "Tarih": "22.03.2026"}
    ]
    st.table(izin_data)
    col_onay1, col_onay2 = st.columns(2)
    with col_onay1: st.button("✅ Seçilenleri Onayla")
    with col_onay2: st.button("❌ Seçilenleri Reddet")

# Footer
st.markdown("<center><p style='color:#777; padding:40px;'>Dormify Admin Panel v1.0</p></center>", unsafe_allow_html=True)