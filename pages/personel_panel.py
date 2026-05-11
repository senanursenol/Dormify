import base64
import streamlit as st
from typing import Dict

# Sistem modülleri ve oturum yönetimi sabitleri
from core.auth import get_display_name, logout, redirect_if_not_logged_in
from core.constants import (
    ROLE_STAFF,
    STAFF_LOGIN_PAGE,
    SESSION_ADMIN_SUB_PAGE,
)
from core.styles import load_student_panel_page_styles

# API Servis katmanının dahil edilmesi
from services.api_service import (
    get_announcements,
    get_meal_menu,
    get_all_faults,
    update_fault_api,
    post_announcement,
    update_meal_api,
    create_student_api,
    delete_announcement_api,
    delete_fault_api,
    get_fault_image_api  # <--- Bunu eklemiştik, duruyor
)

# İstatistikleri hesaplayan fonksiyonu dahil ediyoruz
from services.fault_service import get_status_counts


def decode_base64_image(image_value):
    if not isinstance(image_value, str) or not image_value:
        return image_value

    if image_value.startswith("data:image"):
        try:
            _, _, data = image_value.partition(",")
            return base64.b64decode(data)
        except Exception:
            return image_value

    try:
        return base64.b64decode(image_value)
    except Exception:
        return image_value


def init_admin_state() -> None:
    """Yönetim panelinin başlangıç durumlarını hazırlar."""
    if SESSION_ADMIN_SUB_PAGE not in st.session_state:
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"


def render_topbar(staff_name: str) -> None:
    """Panelin en üstündeki başlık ve bildirimleri içeren profil alanını oluşturur."""
    
    # BİLDİRİM VERİSİNİ ÇEK: Sadece "Beklemede" olanlar yeni bildirim sayılır
    all_faults = get_all_faults()
    pending_faults = [f for f in all_faults if f.get("durum") == "Beklemede"]
    notif_count = len(pending_faults)

    col_left, col_notif, col_right = st.columns([5, 1.5, 1.5])

    with col_left:
        st.markdown(
            f"""
            <div class="topbar-wrap">
                <div style="font-size: 1.4rem; font-weight: 800; color: #1e293b;">
                    ⚙️ Personel Kontrol Paneli
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_notif:
        # BİLDİRİM ÇEKMECESİ
        btn_label = f"🔔 Bildirimler ({notif_count})" if notif_count > 0 else "🔔 Bildirimler"
        with st.popover(btn_label, use_container_width=True):
            st.markdown("#### 📩 Yeni Arıza Kayıtları")
            st.caption("Detaya gidilen bildirimler listeden düşer.")
            st.divider()
            
            if not pending_faults:
                st.info("Yeni bildirim bulunmuyor.")
            else:
                for f in pending_faults[:5]: # Son 5 bildirimi göster
                    with st.container(border=True):
                        st.markdown(f"**📍 Oda {f.get('oda_no')}**")
                        st.caption(f"📝 {f.get('baslik')}")
                        
                        if st.button("Detaya Git", key=f"notif_btn_{f.get('id')}", use_container_width=True):
                            # Bildirimi "Beklemede" durumundan çıkarıyoruz (Silinmiş gibi olur)
                            update_fault_api(f.get('id'), "İnceleniyor")
                            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
                            st.cache_data.clear()
                            st.rerun()

    with col_right:
        with st.popover(f"{staff_name} 👤", use_container_width=True):
            st.markdown("### Hesap Menüsü")
            if st.button("🚪 Çıkış Yap", use_container_width=True):
                logout()
                st.switch_page(STAFF_LOGIN_PAGE)


def render_menu_cards() -> None:
    """Ana sayfadaki 4 ana işlem kartını oluşturur."""
    all_faults = get_all_faults()
    p_count, _, _ = get_status_counts(all_faults)

    st.markdown("""
        <style>
        .info-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 10px;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }
        .info-card h3 { margin: 0 0 10px 0; font-size: 1.1rem; color: #1e293b; }
        .info-card p { margin: 0; font-size: 0.85rem; color: #64748b; line-height: 1.4; }
        </style>
    """, unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        st.markdown('<div class="info-card"><h3>📢 Duyuru Yönetimi</h3><p>Görselli ve Slider destekli duyurular oluşturun.</p></div>', unsafe_allow_html=True)
        if st.button("Duyuruları Düzenle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "duyuru"
            st.cache_data.clear()
            st.rerun()

    with row1_col2:
        st.markdown('<div class="info-card"><h3>🍴 Yemek Menüsü</h3><p>Günlük ve aylık menüleri güncelleyin.</p></div>', unsafe_allow_html=True)
        if st.button("Menüyü Güncelle", use_container_width=True):
            st.switch_page("pages/yemek_listesi.py")

    with row2_col1:
        notif_badge = f' <span style="color:red;">({p_count})</span>' if p_count > 0 else ""
        st.markdown(f'<div class="info-card"><h3>🛠️ Arıza Takibi{notif_badge}</h3><p>Gelen teknik arıza bildirimlerini yönetin.</p></div>', unsafe_allow_html=True)
        if st.button("Arızaları Görüntüle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
            st.cache_data.clear()
            st.rerun()

    with row2_col2:
        st.markdown('<div class="info-card"><h3>👤 Öğrenci Kaydı</h3><p>Sisteme yeni öğrenci hesapları tanımlayın.</p></div>', unsafe_allow_html=True)
        if st.button("Yeni Öğrenci Ekle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ogrenci_ekle"
            st.cache_data.clear()
            st.rerun()


def render_back() -> None:
    if st.button("← Panel Menüsüne Dön"):
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"
        st.cache_data.clear()
        st.rerun()


def render_announcement_page() -> None:
    render_back()
    st.title("📢 Duyuru Yönetimi")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("Yeni Duyuru Ekle")
        with st.container(border=True):
            yeni_baslik = st.text_input("Duyuru Başlığı")
            yeni_icerik = st.text_area("Duyuru İçeriği", height=150)
            yeni_gorsel = st.file_uploader("📷 Duyuru Görseli", type=["png", "jpg", "jpeg"])

            if yeni_gorsel:
                st.image(yeni_gorsel, caption="Önizleme", use_container_width=True)
            
            if st.button("🚀 Duyuruyu Yayınla", type="primary", use_container_width=True):
                if yeni_baslik.strip() and yeni_icerik.strip():
                    res = post_announcement(yeni_baslik.strip(), yeni_icerik.strip(), gorsel=yeni_gorsel)
                    if res.get("status") == "success":
                        st.success("Duyuru başarıyla yayınlandı!")
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.warning("Lütfen alanları doldurun.")
                    
    with col2:
        st.subheader("Mevcut Duyurular")
        mevcut_duyurular = get_announcements()
        if not mevcut_duyurular:
            st.info("Duyuru bulunmuyor.")
        else:
            for duyuru in mevcut_duyurular:
                with st.container(border=True):
                    d_img = decode_base64_image(duyuru.get('gorsel'))
                    if d_img: st.image(d_img, use_container_width=True)
                    st.markdown(f"**{duyuru.get('baslik')}**")
                    st.caption(f"📅 {duyuru.get('tarih')}")
                    if st.button("🗑️ Sil", key=f"del_{duyuru.get('id')}", use_container_width=True):
                        delete_announcement_api(duyuru.get('id'))
                        st.cache_data.clear()
                        st.rerun()


# --- ROZETLERİ (Badge) GERİ GETİREN FONKSİYON ---
def get_status_info(fault: Dict) -> tuple[str, str, str]:
    db_durum = fault.get("durum", "Beklemede")

    if db_durum == "Çözüldü":
        return "solved", "Çözüldü", "✅"
    elif db_durum == "İptal Edildi":
        return "cancelled", "İptal Edildi", "❌"
    else:
        return "pending", "Beklemede", "⏳"
# -----------------------------------------------

def render_fault_page() -> None:
    render_back()
    st.subheader("🛠️ Gelen Arıza Bildirimleri")
    faults = get_all_faults()
    p, s, t = get_status_counts(faults)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Beklemede", p)
    col2.metric("Çözüldü", s)
    col3.metric("Toplam", t)
    st.divider()

    for fault in faults:
        fault_id = fault.get('id')
        
        with st.container(border=True):
            ogrenci_no = fault.get('ogrenci_no', 'Bilinmiyor')
            
            # Başlık ve İsim (Değişmedi)
            st.markdown(f"**📍 Oda {fault.get('oda_no')}** | 👤 **Öğrenci:** {ogrenci_no} | 📌 **{fault.get('baslik')}**")
            
            # AÇIKLAMA (Bunu eklemiştik, info kutusu çok şık)
            st.info(f"📝 **Detay:** {fault.get('aciklama', 'Açıklama belirtilmedi.')}")
            
            # 1. GÖRSEL İKİLENMESİNİ ÇÖZMEK VE 2. GÖRSEL KONTROLÜ
            # Görsel için bir yer tutucu oluşturuyoruz
            gorsel_tutucu = st.empty() 

            # Arızada görsel verisi var mı diye kontrol edelim (Veritabanındaki None mu base64 mü?)
            # NOT: Defer komutu yüzünden burası None dönebilir, o zaman butonu göstereceğiz.
            # Kesin çözüm için API listeleme fonksiyonunda (GET faults) görsel_var_mi diye bir boolean döndürmemiz gerekir.
            # Şimdilik butonu gösterip Lazy Loading'i koruyacağız ama ikilenmeyi çözeceğiz.
            
            if st.button("🖼️ Görseli Görüntüle", key=f"img_btn_{fault_id}"):
                with st.spinner("Görsel yükleniyor..."):
                    # Butona basılınca API'ye gidip sadece bu resmi çeker
                    gorsel_base64 = get_fault_image_api(fault_id)
                    if gorsel_base64:
                        g = decode_base64_image(gorsel_base64)
                        if g: 
                            # Görseli BUTONUN DIŞINA (ve üstüne) render ediyoruz
                            #use_container_width=True yerine yeni Streamlit kuralını width="stretch" ile uygulayalım
                            gorsel_tutucu.image(g, width="stretch") 
                    else:
                        gorsel_tutucu.warning("Bu arızaya ait bir görsel bulunmuyor.")

            # 3. RENKLİ ROZETLERİ (Badge) GERİ GETİRME
           
            
            durum_info = get_status_info(fault)
            style, text, icon = durum_info
            
            # Stilin uygulanabilmesi için styles.py içindeki load_student_panel_page_styles'ın
            # "native-badge" sınıfını renklendirmesi gerekir. (Eskiden vardı, geri ekliyoruz)
            st.markdown(f'<div class="native-badge {style}">{icon} {text}</div>', unsafe_allow_html=True)
            
            # card-gap'i butonlardan önce ekleyelim ki resimle butonlar yapışık olmasın
            st.markdown('<div class="card-gap"></div>', unsafe_allow_html=True)

            # 4. SİL BUTONU VE KEY BENZERSİZLİĞİ
            # Butonların key'lerini daha benzersiz ve sağlam yapıyoruz.
            c1, c2, c3 = st.columns(3)
            if c1.button("✅ Çözüldü", key=f"cozuldu_butonu_{fault_id}"):
                update_fault_api(fault_id, "Çözüldü")
                st.cache_data.clear()
                st.rerun()
            if c2.button("❌ İptal", key=f"iptal_butonu_{fault_id}"):
                update_fault_api(fault_id, "İptal Edildi")
                st.cache_data.clear()
                st.rerun()
            # Sil butonunun key'ini `sil_butonu_{fault_id}` olarak güncelledik, bu sefer silmeli!
            if c3.button("🗑️ Sil", key=f"sil_butonu_{fault_id}", type="primary"):
                delete_fault_api(fault_id)
                st.cache_data.clear()
                st.rerun()


def render_student_add_page() -> None:
    render_back()
    st.subheader("👤 Yeni Öğrenci Kaydı")
    with st.container(border=True):
        fn = st.text_input("Ad Soyad")
        un = st.text_input("Kullanıcı Adı")
        rn = st.text_input("Oda No")
        ps = st.text_input("Şifre", type="password")
        if st.button("Kaydı Tamamla", type="primary"):
            res = create_student_api(un, ps, fn, rn)
            if res.get("status") == "success": st.success("Öğrenci eklendi!")


def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)
    load_student_panel_page_styles()
    init_admin_state()
    staff_name = get_display_name("Personel")
    render_topbar(staff_name)
    page = st.session_state[SESSION_ADMIN_SUB_PAGE]

    if page == "duyuru": render_announcement_page()
    elif page == "ariza": render_fault_page()
    elif page == "ogrenci_ekle": render_student_add_page()
    else: render_menu_cards()

if __name__ == "__main__":
    main()