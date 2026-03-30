import streamlit as st

from core.auth import login_staff
from core.constants import LOGIN_SELECTION_PAGE, STAFF_PANEL_PAGE
from core.styles import load_student_login_styles, render_login_background_blobs
from core.database import SessionLocal  # Bunu import etmeyi unutma
from core.models import Yonetici


def validate_login_input(username: str, password: str) -> str | None:
    clean_username = username.strip()
    clean_password = password.strip()

    if not clean_username:
        return "Kullanıcı adı boş bırakılamaz."
    if not clean_password:
        return "Şifre boş bırakılamaz."
    if len(clean_username) < 3:
        return "Kullanıcı adı en az 3 karakter olmalıdır."
    if len(clean_password) < 4:
        return "Şifre en az 4 karakter olmalıdır."
    return None


def handle_login(username: str, password: str) -> None:
    clean_username = username.strip()
    clean_password = password.strip()

    # 1. Veritabanı oturumu açalım
    db = SessionLocal()
    try:
        # 2. Veritabanında bu kullanıcıyı arayalım
        admin = db.query(Yonetici).filter(Yonetici.kullanici_adi == clean_username).first()

        # 3. Kullanıcı var mı ve şifre doğru mu?
        if admin and admin.sifre == clean_password:
            login_staff(clean_username, name="Yönetici")
            st.success("Giriş başarılı.")
            st.switch_page(STAFF_PANEL_PAGE)
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
            
    except Exception as e:
        st.error(f"Veritabanı hatası: {e}")
    finally:
        # 4. Bağlantıyı her zaman kapatalım
        db.close()


def render_login_card() -> None:
    st.markdown(
        """
        <div class="login-card">
            <div class="icon-wrap">
                <div class="icon-box">🛡️</div>
            </div>
            <div class="title">Personel Girişi</div>
            <div class="subtitle">Yetkili personel bilgileri ile sisteme giriş yapın</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_form() -> None:
    render_login_card()

    st.markdown('<div class="field-label">Kullanıcı Adı</div>', unsafe_allow_html=True)
    username = st.text_input(
        label="Kullanıcı Adı",
        label_visibility="collapsed",
        placeholder="Kullanıcı adınızı girin",
    )

    st.markdown('<div class="field-label">Şifre</div>', unsafe_allow_html=True)
    password = st.text_input(
        label="Şifre",
        label_visibility="collapsed",
        placeholder="Şifrenizi girin",
        type="password",
    )

    if st.button("Giriş Yap", use_container_width=True):
        error_message = validate_login_input(username, password)
        if error_message:
            st.error(error_message)
        else:
            handle_login(username, password)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Geri Dön", use_container_width=True):
        st.switch_page(LOGIN_SELECTION_PAGE)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-note">
            Yetkili personel girişi. Duyuru, bildirim ve sistem süreçlerini yönetmek için giriş yapınız.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_student_login_styles()
    render_login_background_blobs()
    render_form()


main()