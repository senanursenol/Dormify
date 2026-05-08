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
    update_meal_api,
    create_student_api,
    delete_announcement_api,
    delete_fault_api # Silme fonksiyonu eklendi
)

# İstatistikleri hesaplayan fonksiyonu dahil ediyoruz
from services.fault_service import get_status_counts


def init_admin_state() -> None:
    """Yönetim panelinin başlangıç durumlarını (sayfa navigasyonu) hazırlar."""
    if SESSION_ADMIN_SUB_PAGE not in st.session_state:
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"


def render_topbar(staff_name: str) -> None:
    """Panelin en üstündeki başlık ve bildirimleri içeren profil alanını oluşturur."""
    
    # BİLDİRİM VERİSİNİ ÇEK
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
            st.divider()
            if not pending_faults:
                st.info("Yeni bildirim bulunmuyor.")
            else:
                for f in pending_faults[:5]: # Son 5 bildirimi göster
                    with st.container(border=True):
                        st.markdown(f"**📍 Oda {f.get('oda_no')}**")
                        st.caption(f"📝 {f.get('baslik')}")
                        if st.button("Detaya Git", key=f"notif_btn_{f.get('id')}", use_container_width=True):
                            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
                            st.rerun()

    with col_right:
        with st.popover(f"{staff_name} 👤", use_container_width=True):
            st.markdown("### Hesap Menüsü")
            if st.button("🚪 Çıkış Yap", use_container_width=True):
                logout()
                st.switch_page(STAFF_LOGIN_PAGE)


def render_menu_cards() -> None:
    """Ana sayfadaki 4 ana işlem kartını oluşturur."""

    # Arıza sayısını çekip kart başlığına ekleyelim
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
        .info-card h3 {
            margin: 0 0 10px 0;
            font-size: 1.1rem;
            color: #1e293b;
        }
        .info-card p {
            margin: 0;
            font-size: 0.85rem;
            color: #64748b;
            line-height: 1.4;
        }
        </style>
    """, unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        st.markdown(
            '<div class="info-card"><h3>📢 Duyuru Yönetimi</h3><p>Öğrencilere iletilecek genel duyuruları oluşturun ve sistemde yayınlayın.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Duyuruları Düzenle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "duyuru"
            st.rerun()

    with row1_col2:
        st.markdown(
            '<div class="info-card"><h3>🍴 Yemek Menüsü</h3><p>Aylık yemek listesini güncelleyerek öğrenci paneline yansıtın.</p></div>',
            unsafe_allow_html=True
        )

        if st.button("Menüyü Güncelle", use_container_width=True):
            st.switch_page("pages/yemek_listesi.py")

    with row2_col1:
        # Arıza başlığına dinamik sayı ekledik
        notif_badge = f' <span style="color:red;">({p_count})</span>' if p_count > 0 else ""
        st.markdown(
            f'<div class="info-card"><h3>🛠️ Arıza Takibi{notif_badge}</h3><p>Öğrencilerden gelen teknik arıza bildirimlerini görüntüleyin ve yönetin.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Arızaları Görüntüle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
            st.rerun()

    with row2_col2:
        st.markdown(
            '<div class="info-card"><h3>👤 Öğrenci Kaydı</h3><p>Sisteme yeni katılacak öğrenciler için kullanıcı hesabı ve oda tanımlayın.</p></div>',
            unsafe_allow_html=True
        )
        if st.button("Yeni Öğrenci Ekle", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ogrenci_ekle"
            st.rerun()


def render_back() -> None:
    """Alt sayfalardan ana menüye dönüş butonunu oluşturur."""
    if st.button("← Panel Menüsüne Dön"):
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"
        st.rerun()


def render_student_add_page() -> None:
    render_back()
    st.subheader("👤 Yeni Öğrenci Kaydı")

    with st.container(border=True):
        full_name = st.text_input("Ad Soyad")
        username = st.text_input("Kullanıcı Adı")
        room_no = st.text_input("Oda Numarası")
        password = st.text_input("Şifre", type="password")

        if st.button("Öğrenciyi Kaydet", type="primary", use_container_width=True):
            if not all([full_name.strip(), username.strip(), room_no.strip(), password.strip()]):
                st.warning("Tüm alanları doldurmanız gerekmektedir.")
            else:
                res = create_student_api(
                    username.strip(),
                    password.strip(),
                    full_name.strip(),
                    room_no.strip(),
                )
                if res.get("status") == "success":
                    st.success(f"{full_name.strip()} sisteme başarıyla eklendi!")
                    st.balloons()
                else:
                    st.error(res.get("message", "Öğrenci kaydı sırasında bir hata oluştu."))


def render_stats(pending_count: int, solved_count: int, total_count: int) -> None:
    col1, col2, col3 = st.columns(3)
    box_style = "border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; text-align: center; background-color: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);"

    with col1:
        st.markdown(f'<div style="{box_style}"><div style="font-size: 24px;">⏳</div><div style="font-size: 28px; font-weight: 800; color: #ef4444;">{pending_count}</div><div style="color: #64748b; font-weight: 600;">Beklemede</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div style="{box_style}"><div style="font-size: 24px;">✅</div><div style="font-size: 28px; font-weight: 800; color: #22c55e;">{solved_count}</div><div style="color: #64748b; font-weight: 600;">Çözüldü</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div style="{box_style}"><div style="font-size: 24px;">📋</div><div style="font-size: 28px; font-weight: 800; color: #0f172a;">{total_count}</div><div style="color: #64748b; font-weight: 600;">Toplam</div></div>', unsafe_allow_html=True)


def render_announcement_page() -> None:
    render_back()
    st.title("📢 Duyuru Yönetimi")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("Yeni Duyuru Ekle")
        with st.container(border=True):
            yeni_baslik = st.text_input("Duyuru Başlığı", placeholder="Örn: Teknik Bakım")
            yeni_icerik = st.text_area("Duyuru İçeriği", height=150, placeholder="Duyuru detaylarını buraya yazın...")
            
            if st.button("🚀 Duyuruyu Yayınla", type="primary", use_container_width=True):
                if yeni_baslik.strip() and yeni_icerik.strip():
                    res = post_announcement(yeni_baslik.strip(), yeni_icerik.strip())
                    if res.get("status") == "success":
                        st.success("Duyuru başarıyla yayınlandı!")
                        st.rerun()
                    else:
                        st.error("Bir hata oluştu.")
                else:
                    st.warning("Lütfen başlık ve içerik giriniz.")
                    
    with col2:
        st.subheader("Mevcut Duyurular")
        mevcut_duyurular = get_announcements()
        
        if not mevcut_duyurular:
            st.info("Sistemde aktif bir duyuru bulunmuyor.")
        else:
            for duyuru in mevcut_duyurular:
                with st.container(border=True):
                    st.markdown(f"**{duyuru.get('baslik')}**")
                    st.caption(f"Tarih: {duyuru.get('tarih')}")
                    st.write(duyuru.get('icerik'))
                    
                    if st.button("🗑️ Sil", key=f"del_{duyuru.get('id')}", type="secondary"):
                        delete_announcement_api(duyuru.get('id'))
                        st.rerun()


def render_fault_page() -> None:
    render_back()
    st.subheader("🛠️ Gelen Arıza Bildirimleri")

    faults = get_all_faults()
    pending_count, solved_count, total_count = get_status_counts(faults)

    render_stats(pending_count, solved_count, total_count)
    st.divider()

    if not faults:
        st.info("Şu an sistemde aktif arıza bulunmuyor.")
        return

    for fault in faults:
        fault_id = fault.get("id")
        # Öğrencinin yüklediği görsel verisini API'den alıyoruz
        gorsel_yolu = fault.get("gorsel") 

        with st.container(border=True):
            status = fault.get("durum", "Beklemede")
            durum_rengi = "#ef4444" if status == "Beklemede" else "#22c55e" if status == "Çözüldü" else "#64748b"

            st.markdown(f"**📍 Oda:** {fault.get('oda_no')} | **📌 Başlık:** {fault.get('baslik')}")
            st.markdown(f"**Durum:** <span style='color:{durum_rengi}; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            st.write(f"📝 **Açıklama:** {fault.get('aciklama')}")

            # Eğer bir görsel varsa burada gösteriyoruz
            if gorsel_yolu:
                with st.expander("🖼️ Arıza Görselini Görüntüle"):
                    st.image(gorsel_yolu, caption="Arıza Kanıtı", use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)

            if c1.button("⏳ Beklemede", key=f"p_{fault_id}", use_container_width=True):
                if update_fault_api(fault_id, "Beklemede").get("status") == "success":
                    st.rerun()

            if c2.button("✅ Çözüldü", key=f"s_{fault_id}", use_container_width=True):
                if update_fault_api(fault_id, "Çözüldü").get("status") == "success":
                    st.rerun()

            if c3.button("İptal Et", key=f"c_{fault_id}", use_container_width=True):
                if update_fault_api(fault_id, "İptal Edildi").get("status") == "success":
                    st.rerun()

            if c4.button("🗑️ Sil", key=f"d_{fault_id}", type="primary", use_container_width=True):
                if delete_fault_api(fault_id).get("status") == "success":
                    st.rerun()


def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)
    load_student_panel_page_styles()
    init_admin_state()

    staff_name = get_display_name("Personel")
    render_topbar(staff_name)

    page = st.session_state[SESSION_ADMIN_SUB_PAGE]

    if page == "duyuru":
        render_announcement_page()
    elif page == "ariza":
        render_fault_page()
    elif page == "ogrenci_ekle":
        render_student_add_page()
    else:
        render_menu_cards()


if __name__ == "__main__":
    main()