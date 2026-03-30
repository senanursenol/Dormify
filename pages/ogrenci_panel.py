import streamlit as st

from core.auth import get_display_name, logout, redirect_if_not_logged_in
from core.constants import (
    HOME_PAGE,
    ROLE_STUDENT,
    STUDENT_FAULT_PAGE,
    STUDENT_LOGIN_PAGE,
    STUDENT_NOTIFICATIONS_PAGE,
)
from core.styles import load_student_panel_page_styles
from core.ui import render_logo


def render_topbar(student_name: str) -> None:
    left_col, right_col = st.columns([6, 2])

    with left_col:
        # LOGO BOYUTU BURADA GÜNCELLENDİ: width=140 -> width=170 yapıldı
        render_logo(center=False, width=170)

    with right_col:
        with st.popover(f"{student_name} 👤", use_container_width=True):
            st.markdown("### Hesap Menüsü")
            st.caption("İşlem seçin")

            # Boş kutu yaratan '<div class="menu-btn">' HTML kodları temizlendi
            if st.button("🚪 Çıkış Yap", use_container_width=True, key="cikis_menu"):
                logout()
                st.switch_page(HOME_PAGE)


def render_welcome(student_name: str) -> None:
    st.markdown(
        f"""
        <div class="welcome-wrap">
            <div class="welcome-title">Hoş geldin {student_name}</div>
            <div class="welcome-subtitle">Yurt işlemlerinizi kolayca yönetin</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_main_actions() -> None:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="icon-badge">🛠️</div>
                <div class="card-title">Arıza Bildirimi</div>
                <div class="card-text">
                    Odada veya ortak alanlarda tespit ettiğiniz arızaları hızlıca bildirin.
                    Personelimiz en kısa sürede çözüm sürecini başlatacaktır.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Boş kutu yaratan '<div class="primary-btn">' HTML kodları temizlendi
        if st.button("➕ Yeni Arıza Bildir", use_container_width=True, key="new_fault_button"):
            st.switch_page(STUDENT_FAULT_PAGE)

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="icon-badge">🔔</div>
                <div class="card-title">Bildirimlerim</div>
                <div class="card-text">
                    Gönderdiğiniz arıza kayıtlarını takip edin, güncel durumlarını görüntüleyin
                    ve süreçleri tek ekrandan yönetin.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Boş kutu yaratan HTML kodları temizlendi
        if st.button("📋 Bildirimleri Gör", use_container_width=True, key="show_notifications_button"):
            st.switch_page(STUDENT_NOTIFICATIONS_PAGE)

    st.markdown(
        """
        <div class="info-box">
            Öğrenci panelinden arıza bildirimlerinizi oluşturabilir ve sistem duyurularınızı takip edebilirsiniz.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)
    load_student_panel_page_styles()

    student_name = get_display_name("Öğrenci")

    render_topbar(student_name)
    render_welcome(student_name)
    render_main_actions()


main()