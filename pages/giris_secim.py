import streamlit as st

from core.constants import HOME_PAGE, STUDENT_LOGIN_PAGE, STAFF_LOGIN_PAGE
from core.styles import load_landing_styles
from core.ui import render_logo


def configure_page() -> None:
    st.set_page_config(
        page_title="Dormify | Güvenli & Modern",
        page_icon="🏢",
        layout="centered",
    )


def render_header() -> None:
    render_logo()

    st.markdown(
        """
        <div class="title">Hoş Geldiniz</div>
        <div class="subtitle">Lütfen giriş türünü seçin</div>
        """,
        unsafe_allow_html=True,
    )


def render_login_buttons() -> None:
    if st.button("🎓 Öğrenci Girişi", use_container_width=True):
        st.switch_page(STUDENT_LOGIN_PAGE)

    if st.button("🛡️ Personel Girişi", use_container_width=True):
        st.switch_page(STAFF_LOGIN_PAGE)


def render_footer() -> None:
    st.markdown(
        """
        <div class="divider">veya</div>
        <div class="support">📞 0531 695 99 62 / 📧 beylikduzu.kiz.yurdu@ensar.org</div>
        
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Ana Sayfaya Dön", use_container_width=True):
        st.switch_page(HOME_PAGE)
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    configure_page()
    load_landing_styles()
    render_header()
    render_login_buttons()
    render_footer()


main()