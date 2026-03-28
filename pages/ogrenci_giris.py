import streamlit as st

from core.auth import login_student
from core.constants import HOME_PAGE, STUDENT_PANEL_PAGE
from core.styles import load_student_login_styles, render_login_background_blobs


def validate_login_input(student_number: str, password: str) -> str | None:
    clean_student_number = student_number.strip()
    clean_password = password.strip()

    if not clean_student_number:
        return "Öğrenci numarası boş bırakılamaz."
    if not clean_password:
        return "Şifre boş bırakılamaz."
    if not clean_student_number.isdigit():
        return "Öğrenci numarası yalnızca rakamlardan oluşmalıdır."
    if len(clean_student_number) < 4:
        return "Öğrenci numarası en az 4 haneli olmalıdır."
    if len(clean_password) < 4:
        return "Şifre en az 4 karakter olmalıdır."
    return None


def handle_login(student_number: str) -> None:
    login_student(student_number)
    st.success("Giriş başarılı.")
    st.switch_page(STUDENT_PANEL_PAGE)


def render_login_card() -> None:
    st.markdown(
        """
        <div class="login-card">
            <div class="icon-wrap">
                <div class="icon-box">🎓</div>
            </div>
            <div class="title">Öğrenci Girişi</div>
            <div class="subtitle">Öğrenci numaranız ve şifreniz ile sisteme giriş yapın</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_form() -> None:
    render_login_card()

    st.markdown('<div class="field-label">Öğrenci No</div>', unsafe_allow_html=True)
    student_number = st.text_input(
        label="Öğrenci No",
        label_visibility="collapsed",
        placeholder="Öğrenci numaranızı girin",
        max_chars=10,
    )

    st.markdown('<div class="field-label">Şifre</div>', unsafe_allow_html=True)
    password = st.text_input(
        label="Şifre",
        label_visibility="collapsed",
        placeholder="Şifrenizi girin",
        type="password",
    )

    if st.button("Giriş Yap", use_container_width=True):
        error_message = validate_login_input(student_number, password)
        if error_message:
            st.error(error_message)
        else:
            handle_login(student_number)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Geri Dön", use_container_width=True):
        st.switch_page(HOME_PAGE)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-note">
            Güvenli giriş altyapısı ile öğrenci işlemlerinizi hızlı ve düzenli şekilde yönetin.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_student_login_styles()
    render_login_background_blobs()
    render_form()


main()