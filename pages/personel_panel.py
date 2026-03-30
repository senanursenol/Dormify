import streamlit as st

# Sistem modülleri ve oturum yönetimi sabitleri
from core.auth import get_display_name, logout, redirect_if_not_logged_in
from core.constants import (
    ROLE_STAFF,
    STAFF_LOGIN_PAGE,
    SESSION_ADMIN_SUB_PAGE,
)
from core.styles import load_student_panel_page_styles

# API Servis katmanının dahil edilmesi
# Buradaki fonksiyonlar api_service.py dosyasında tanımladığımız elçilerdir.
from services.api_service import (
    get_announcements, 
    get_meal_menu, 
    get_all_faults,
    update_fault_api,
    post_announcement,  # Yeni eklediğimiz duyuru gönderici
    update_meal_api     # Yeni eklediğimiz yemek güncelleyici
)

def init_admin_state() -> None:
    """Yönetim panelinin başlangıç durumlarını (sayfa navigasyonu) hazırlar."""
    if SESSION_ADMIN_SUB_PAGE not in st.session_state:
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"

def render_topbar(staff_name: str) -> None:
    """Panelin en üstündeki başlık ve kullanıcı profil alanını oluşturur."""
    col_left, col_right = st.columns([6, 2])

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

    with col_right:
        with st.popover(f"{staff_name} 👤", use_container_width=True):
            st.markdown("### Hesap Menüsü")
            if st.button("🚪 Çıkış Yap", use_container_width=True):
                logout()
                st.switch_page(STAFF_LOGIN_PAGE)


def render_menu_cards() -> None:
    """Ana sayfadaki 3 ana işlem kartını (Duyuru, Yemek, Arıza) oluşturur."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="feature-card"><h3>📢 Duyuru Yönetimi</h3></div>', unsafe_allow_html=True)
        if st.button("Duyuruları Düzenle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "duyuru"
            st.rerun()

    with col2:
        st.markdown('<div class="feature-card"><h3>🍴 Yemek Menüsü</h3></div>', unsafe_allow_html=True)
        if st.button("Menüyü Güncelle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "yemek"
            st.rerun()

    with col3:
        st.markdown('<div class="feature-card"><h3>🛠️ Arıza Takibi</h3></div>', unsafe_allow_html=True)
        if st.button("Arızaları Görüntüle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
            st.rerun()


def render_back() -> None:
    """Alt sayfalardan ana menüye dönüş butonunu oluşturur."""
    if st.button("← Panel Menüsüne Dön"):
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"
        st.rerun()


# ---------------- DUYURU YÖNETİMİ (GÜNCELLENDİ) ----------------
def render_announcement_page() -> None:
    """Yeni duyuru ekleme sayfası - API bağlantısı eklendi."""
    render_back()
    st.subheader("Yeni Duyuru Yayınla")
    
    title = st.text_input("Duyuru Başlığı", placeholder="Örn: Teknik Bakım")
    content = st.text_area("Duyuru İçeriği", placeholder="Duyuru detaylarını buraya yazın...")
    
    if st.button("Sistemde Yayınla", type="primary", use_container_width=True):
        if not title.strip() or not content.strip():
            st.warning("Lütfen başlık ve içerik alanlarını doldurun.")
        else:
            # API'ye yeni duyuruyu gönderiyoruz
            res = post_announcement(title, content)
            if res.get("status") == "success":
                st.success("Duyuru tüm öğrencilere başarıyla iletildi!")
                st.balloons() # Başarı kutlaması
            else:
                st.error("Duyuru yayınlanırken bir hata oluştu.")


# ---------------- YEMEK MENÜSÜ YÖNETİMİ (GÜNCELLENDİ) ----------------
def render_menu_page() -> None:
    """Günün yemek menüsünü API'den çeker ve günceller."""
    render_back()
    st.subheader("Günlük Yemek Listesi")
    
    # Mevcut menüyü FastAPI'den çekip kutuya yazıyoruz
    current_menu = get_meal_menu()
    menu_value = st.text_area("Menü Detayları (Örn: Çorba, Ana Yemek, Pilav)", value=current_menu)
    
    if st.button("Tüm Sistemde Güncelle", type="primary", use_container_width=True):
        # API'ye menü güncelleme isteği (PUT) gönderiyoruz
        res = update_meal_api(menu_value)
        if res.get("status") == "success":
            st.success("Yemek menüsü başarıyla güncellendi!")
        else:
            st.error("Menü güncellenirken bir hata oluştu.")


# ---------------- ARIZA TAKİP SAYFASI ----------------
def render_fault_page() -> None:
    render_back()
    st.subheader("🛠️ Gelen Arıza Bildirimleri")

    # Arızaları API'den (dolayısıyla veritabanından) çekiyoruz
    faults = get_all_faults()

    if not faults:
        st.info("Şu an sistemde aktif arıza bulunmuyor.")
        return

    st.divider()
    
    for fault in faults:
        # Veritabanındaki gerçek ID'yi alıyoruz (Eski kodda 'i' kullanılıyordu)
        fault_id = fault.get("id") 
        
        with st.container(border=True):
            # Duruma göre renk belirleme
            status = fault.get("durum", "Beklemede")
            if status == "Beklemede":
                durum_rengi = "#ef4444" # Kırmızı
            elif status == "Çözüldü":
                durum_rengi = "#22c55e" # Yeşil
            else:
                durum_rengi = "#64748b" # Gri (İptal)
            
            st.markdown(f"**📍 Oda:** {fault.get('oda_no')} | **📌 Başlık:** {fault.get('baslik')}")
            st.markdown(f"**Durum:** <span style='color:{durum_rengi}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            st.write(f"📝 **Açıklama:** {fault.get('aciklama')}") # Key ismini veritabanı modelinle aynı yap ('aciklama')
            
            # DURUM GÜNCELLEME BUTONLARI
            # Personel_panel.py dosyasındaki BUTONLAR kısmını bununla değiştir:
            
            # Artık 3 değil, 4 kolonumuz var!
            c1, c2, c3, c4 = st.columns(4)
            
            if c1.button("⏳ Beklemede", key=f"p_{fault_id}", use_container_width=True):
                res = update_fault_api(fault_id, "Beklemede")
                if res.get("status") == "success": st.rerun()

            if c2.button("✅ Çözüldü", key=f"s_{fault_id}", use_container_width=True):
                res = update_fault_api(fault_id, "Çözüldü")
                if res.get("status") == "success": st.rerun()

            if c3.button("❌ İptal Et", key=f"c_{fault_id}", use_container_width=True):
                res = update_fault_api(fault_id, "İptal Edildi")
                if res.get("status") == "success": st.rerun()

            # YENİ EKLENEN SİLME BUTONU
            if c4.button("🗑️ Sil", key=f"d_{fault_id}", type="primary", use_container_width=True):
                from services.api_service import delete_fault_api # Silme fonksiyonunu çağır
                res = delete_fault_api(fault_id)
                if res.get("status") == "success": 
                    st.toast("Arıza kalıcı olarak silindi!", icon="🗑️")
                    st.rerun()
# ---------------- ANA DÖNGÜ (MAIN) ----------------
def main() -> None:
    """Personel paneli giriş ve sayfa yönetimi."""
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)
    load_student_panel_page_styles()
    init_admin_state()

    staff_name = get_display_name("Personel")
    render_topbar(staff_name)

    page = st.session_state[SESSION_ADMIN_SUB_PAGE]

    # Sayfa yönlendirmesi
    if page == "duyuru":
        render_announcement_page()
    elif page == "yemek":
        render_menu_page()
    elif page == "ariza":
        render_fault_page()
    else:
        render_menu_cards()


if __name__ == "__main__":
    main()