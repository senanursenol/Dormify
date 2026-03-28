import streamlit as st

from core.constants import STUDENT_LOGIN_PAGE, STAFF_LOGIN_PAGE
from core.styles import load_landing_styles
from core.ui import render_logo


def configure_page() -> None:
    st.set_page_config(
        page_title="Dormify | Güvenli & Modern",
        page_icon="🏢",
        layout="centered",
    )


def render_home() -> None:
    render_logo()

    st.markdown(
        """
        <div class="title">Hoş Geldiniz</div>
        <div class="subtitle">Hesabınıza giriş yapın</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🎓 Öğrenci Girişi", use_container_width=True):
        st.switch_page(STUDENT_LOGIN_PAGE)

    if st.button("🛡️ Personel Girişi", use_container_width=True):
        st.switch_page(STAFF_LOGIN_PAGE)

    st.markdown(
        """
        <div class="divider">veya</div>
        <div class="support">📞 0850 123 45 67</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    configure_page()
    load_landing_styles()
    render_home()


main()