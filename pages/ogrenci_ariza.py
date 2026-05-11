import streamlit as st

from core.auth import get_student_no, redirect_if_not_logged_in
from core.constants import (
    ROLE_STUDENT,
    SESSION_FAULT_SENT,
    STUDENT_LOGIN_PAGE,
    STUDENT_PANEL_PAGE,
)
from core.styles import load_student_fault_page_styles

from services.api_service import send_fault_report


def init_page_state() -> None:
    if SESSION_FAULT_SENT not in st.session_state:
        st.session_state[SESSION_FAULT_SENT] = False


def render_header() -> None:
    st.markdown(
        """
        <div class="header-card">
            <div class="header-icon">🛠️</div>
            <div class="header-title">Arıza Bildirimi</div>
            <div class="header-subtitle">
                Arıza kaydınızı oluşturun, çözüm için hemen inceleyelim.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def validate_form(description: str, uploaded_image) -> str | None:
    if not description.strip():
        return "Arıza açıklaması boş bırakılamaz."

    if len(description.strip()) < 10:
        return "Arıza açıklaması en az 10 karakter olmalıdır."

    if uploaded_image is not None:
        allowed_types = ["image/png", "image/jpeg", "image/jpg"]

        if uploaded_image.type not in allowed_types:
            return "Sadece PNG, JPG veya JPEG formatında görsel yükleyebilirsiniz."

        max_size_mb = 5
        max_size_byte = max_size_mb * 1024 * 1024

        if uploaded_image.size > max_size_byte:
            return f"Görsel boyutu en fazla {max_size_mb} MB olabilir."

    return None


def go_to_panel() -> None:
    st.session_state[SESSION_FAULT_SENT] = False
    st.switch_page(STUDENT_PANEL_PAGE)


def render_form(student_number: str) -> None:

    st.markdown('<div class="field-label">📝 Arıza Açıklama</div>', unsafe_allow_html=True)
    description = st.text_area(
        "Arıza Açıklama",
        label_visibility="collapsed",
        placeholder="Arızayı detaylı açıklayın.",
    )

    st.markdown('<div class="field-label">📷 Arıza Görseli</div>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader(
        "Arıza Görseli",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed",
        help="İsterseniz arızaya ait bir fotoğraf yükleyebilirsiniz."
    )

    if uploaded_image is not None:
        st.image(
            uploaded_image,
            caption="Yüklenen arıza görseli",
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Bildirimi Gönder", use_container_width=True):
            error_message = validate_form(description, uploaded_image)

            if error_message:
                st.error(error_message)
            else:
                with st.spinner("Bildiriminiz FastAPI üzerinden iletiliyor..."):
                    result = send_fault_report(
                        baslik="Arıza Bildirimi",
                        detay=description,
                        ogrenci_no=student_number,
                        gorsel=uploaded_image
                    )

                if result["status"] == "success":
                    # --- SİHİRLİ DOKUNUŞ BURADA ---
                    st.cache_data.clear() # Tüm önbelleği siler, sistemi yeni verileri anında çekmeye zorlar!
                    # ------------------------------
                    st.session_state[SESSION_FAULT_SENT] = True
                    st.rerun()
                else:
                    st.error(f"⚠️ API Hatası: {result.get('message', 'Sunucuya ulaşılamadı.')}")

    with col2:
        if st.button("Panele Dön", use_container_width=True):
            go_to_panel()

    st.markdown(
        """
        <div class="info-box">
            Oluşturduğunuz arıza kaydı personel paneli üzerinden takip edilebilir.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success() -> None:
    st.markdown(
        """
        <div class="success-card">
            <div class="success-icon">✅</div>
            <div class="success-title">Bildiriminiz Başarıyla Gönderildi!</div>
            <div class="success-text">
                Arıza bildiriminiz sisteme kaydedildi.<br>
                Personel ekibimiz en kısa sürede çözüm üretecek.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏠 Panele Dön", use_container_width=True):
            go_to_panel()

    with col2:
        if st.button("➕ Yeni Bildirim", use_container_width=True):
            st.session_state[SESSION_FAULT_SENT] = False
            st.rerun()


def main() -> None:
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)

    init_page_state()
    load_student_fault_page_styles()
    render_header()

    student_number = get_student_no()

    if st.session_state[SESSION_FAULT_SENT]:
        render_success()
    else:
        render_form(student_number)


if __name__ == "__main__":
    main()