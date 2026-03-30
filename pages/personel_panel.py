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
from services.api_service import (
    get_announcements, 
    get_meal_menu, 
    get_all_faults,
    update_fault_api,
    post_announcement,
    update_meal_api
)

# İstatistikleri hesaplayan fonksiyonu dahil ediyoruz
from services.fault_service import get_status_counts


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

# ---------------- YENİ EKLENEN İSTATİSTİK KARTLARI ----------------
def render_stats(pending_count: int, solved_count: int, total_count: int) -> None:
    """Sayfanın üst kısmında istatistik kartlarını kutu (card) tasarımıyla gösterir."""
    col1, col2, col3 = st.columns(3)

    # Kutuların şık görünmesi için arka plan, kenarlık ve gölge (shadow) ayarlarımız
    box_style = """
        border: 1px solid #e2e8f0; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center; 
        background-color: #ffffff; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    """

    with col1:
        st.markdown(
            f"""
            <div style="{box_style}">
                <div style="font-size: 24px; margin-bottom: 5px;">⏳</div>
                <div style="font-size: 28px; font-weight: 800; color: #ef4444;">{pending_count}</div>
                <div style="color: #64748b; font-size: 15px; font-weight: 600;">Beklemede</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{box_style}">
                <div style="font-size: 24px; margin-bottom: 5px;">✅</div>
                <div style="font-size: 28px; font-weight: 800; color: #22c55e;">{solved_count}</div>
                <div style="color: #64748b; font-size: 15px; font-weight: 600;">Çözüldü</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{box_style}">
                <div style="font-size: 24px; margin-bottom: 5px;">📋</div>
                <div style="font-size: 28px; font-weight: 800; color: #0f172a;">{total_count}</div>
                <div style="color: #64748b; font-size: 15px; font-weight: 600;">Toplam</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------- DUYURU YÖNETİMİ ----------------
def render_announcement_page() -> None:
    render_back()
    st.subheader("Yeni Duyuru Yayınla")
    
    title = st.text_input("Duyuru Başlığı", placeholder="Örn: Teknik Bakım")
    content = st.text_area("Duyuru İçeriği", placeholder="Duyuru detaylarını buraya yazın...")
    
    if st.button("Sistemde Yayınla", type="primary", use_container_width=True):
        if not title.strip() or not content.strip():
            st.warning("Lütfen başlık ve içerik alanlarını doldurun.")
        else:
            res = post_announcement(title, content)
            if res.get("status") == "success":
                st.success("Duyuru tüm öğrencilere başarıyla iletildi!")
                st.balloons()
            else:
                st.error("Duyuru yayınlanırken bir hata oluştu.")


# ---------------- YEMEK MENÜSÜ YÖNETİMİ ----------------
def render_menu_page() -> None:
    render_back()
    st.subheader("Günlük Yemek Listesi")
    
    current_menu = get_meal_menu()
    menu_value = st.text_area("Menü Detayları (Örn: Çorba, Ana Yemek, Pilav)", value=current_menu)
    
    if st.button("Tüm Sistemde Güncelle", type="primary", use_container_width=True):
        res = update_meal_api(menu_value)
        if res.get("status") == "success":
            st.success("Yemek menüsü başarıyla güncellendi!")
        else:
            st.error("Menü güncellenirken bir hata oluştu.")


# ---------------- ARIZA TAKİP SAYFASI ----------------
def render_fault_page() -> None:
    render_back()
    st.subheader("🛠️ Gelen Arıza Bildirimleri")

    # Arızaları API'den çekiyoruz
    faults = get_all_faults()

    # İstatistikleri hesaplayıp hemen başlığın altına basıyoruz
    pending_count, solved_count, total_count = get_status_counts(faults)
    render_stats(pending_count, solved_count, total_count)
    
    st.divider()

    if not faults:
        st.info("Şu an sistemde aktif arıza bulunmuyor.")
        return
    
    for fault in faults:
        fault_id = fault.get("id") 
        
        with st.container(border=True):
            status = fault.get("durum", "Beklemede")
            if status == "Beklemede":
                durum_rengi = "#ef4444" 
            elif status == "Çözüldü":
                durum_rengi = "#22c55e" 
            else:
                durum_rengi = "#64748b" 
            
            st.markdown(f"**📍 Oda:** {fault.get('oda_no')} | **📌 Başlık:** {fault.get('baslik')}")
            st.markdown(f"**Durum:** <span style='color:{durum_rengi}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            st.write(f"📝 **Açıklama:** {fault.get('aciklama')}") 
            
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

            if c4.button("🗑️ Sil", key=f"d_{fault_id}", type="primary", use_container_width=True):
                from services.api_service import delete_fault_api 
                res = delete_fault_api(fault_id)
                if res.get("status") == "success": 
                    st.toast("Arıza kalıcı olarak silindi!", icon="🗑️")
                    st.rerun()

# ---------------- ANA DÖNGÜ (MAIN) ----------------
def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)
    load_student_panel_page_styles()
    init_admin_state()

    staff_name = get_display_name("Personel")
    render_topbar(staff_name)

    page = st.session_state[SESSION_ADMIN_SUB_PAGE]

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