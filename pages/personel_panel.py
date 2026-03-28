import streamlit as st

from core.auth import get_display_name, logout, redirect_if_not_logged_in
from core.constants import (
    ROLE_STAFF,
    STAFF_LOGIN_PAGE,
    STATUS_CANCELLED,
    STATUS_PENDING,
    STATUS_SOLVED,
    SESSION_ADMIN_SUB_PAGE,
    SESSION_ANNOUNCEMENTS,
    SESSION_MEAL_MENU,
)
from core.styles import load_student_panel_page_styles
from services.fault_service import (
    get_all_faults,
    get_status_counts,
    get_status_label,
    init_fault_state,
    update_fault_status,
)


def init_admin_state() -> None:
    init_fault_state()

    if SESSION_ADMIN_SUB_PAGE not in st.session_state:
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"

    if SESSION_ANNOUNCEMENTS not in st.session_state:
        st.session_state[SESSION_ANNOUNCEMENTS] = []

    if SESSION_MEAL_MENU not in st.session_state:
        st.session_state[SESSION_MEAL_MENU] = "Yayla Çorbası, Tavuk Sote, Pilav, Meyve"


def render_topbar(staff_name: str) -> None:
    col_left, col_right = st.columns([6, 2])

    with col_left:
        st.markdown(
            """
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
            st.caption("İşlem seçin")

            if st.button("🚪 Çıkış Yap", use_container_width=True):
                logout()
                st.switch_page(STAFF_LOGIN_PAGE)


def render_menu_cards() -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="feature-card"><h3>📢 Duyuru</h3></div>', unsafe_allow_html=True)
        if st.button("Duyuru Sayfasına Git", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "duyuru"
            st.rerun()

    with col2:
        st.markdown('<div class="feature-card"><h3>🍴 Yemek</h3></div>', unsafe_allow_html=True)
        if st.button("Yemek Sayfasına Git", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "yemek"
            st.rerun()

    with col3:
        st.markdown('<div class="feature-card"><h3>🛠️ Arıza</h3></div>', unsafe_allow_html=True)
        if st.button("Arıza Sayfasına Git", use_container_width=True):
            st.session_state[SESSION_ADMIN_SUB_PAGE] = "ariza"
            st.rerun()


def render_back() -> None:
    if st.button("← Panel Menüsüne Dön"):
        st.session_state[SESSION_ADMIN_SUB_PAGE] = "secim"
        st.rerun()


# ---------------- DUYURU ----------------
def render_announcement_page() -> None:
    render_back()

    title = st.text_input("Başlık")
    content = st.text_area("İçerik")

    if st.button("Yayınla", type="primary"):
        if not title.strip():
            st.error("Başlık boş bırakılamaz.")
        elif not content.strip():
            st.error("İçerik boş bırakılamaz.")
        else:
            st.session_state[SESSION_ANNOUNCEMENTS].insert(
                0,
                {
                    "baslik": title.strip(),
                    "icerik": content.strip(),
                    "etiket": "YENİ",
                    "renk": "#3b82f6",
                },
            )
            st.success("Duyuru eklendi.")


# ---------------- YEMEK ----------------
def render_menu_page() -> None:
    render_back()

    menu_value = st.text_area(
        "Menü",
        value=st.session_state[SESSION_MEAL_MENU],
    )

    if st.button("Güncelle", type="primary"):
        st.session_state[SESSION_MEAL_MENU] = menu_value
        st.success("Menü güncellendi.")


# ---------------- ARIZA ----------------
def render_fault_page() -> None:
    render_back()

    faults = get_all_faults()

    if not faults:
        st.info("Arıza kaydı yok.")
        return

    pending, solved, total = get_status_counts(faults)

    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam", total)
    col2.metric("Beklemede", pending)
    col3.metric("Çözüldü", solved)

    for i, fault in enumerate(faults):
        st.write(f"🚪 Oda {fault.get('oda_no')} - {fault.get('aciklama')}")

        c1, c2, c3 = st.columns(3)

        if c1.button("Beklemede", key=f"p{i}"):
            update_fault_status(fault["id"], STATUS_PENDING)
            st.rerun()

        if c2.button("Çözüldü", key=f"s{i}"):
            update_fault_status(fault["id"], STATUS_SOLVED)
            st.rerun()

        if c3.button("İptal", key=f"c{i}"):
            update_fault_status(fault["id"], STATUS_CANCELLED)
            st.rerun()


# ---------------- MAIN ----------------
def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)

    load_student_panel_page_styles()
    init_admin_state()

    name = get_display_name("Personel")
    render_topbar(name)

    page = st.session_state[SESSION_ADMIN_SUB_PAGE]

    if page == "duyuru":
        render_announcement_page()
    elif page == "yemek":
        render_menu_page()
    elif page == "ariza":
        render_fault_page()
    else:
        render_menu_cards()


main()