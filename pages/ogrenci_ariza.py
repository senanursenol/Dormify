import streamlit as st

# Uygulamanın temel modüllerini ve sabitlerini içeri aktarıyoruz
from core.auth import get_student_no, redirect_if_not_logged_in
from core.constants import (
    ROLE_STUDENT,
    SESSION_FAULT_SENT,
    STUDENT_LOGIN_PAGE,
    STUDENT_PANEL_PAGE,
)
from core.styles import load_student_fault_page_styles

# API ile iletişim kuran servis fonksiyonumuzu dahil ediyoruz
# Bu katman, UI ile Backend (FastAPI) arasındaki köprüdür.
from services.api_service import send_fault_report

def init_page_state() -> None:
    """
    Sayfanın çalışma durumunu (Session State) başlatır.
    'SESSION_FAULT_SENT': Kullanıcının bildirim gönderip göndermediğini takip eder.
    """
    if SESSION_FAULT_SENT not in st.session_state:
        st.session_state[SESSION_FAULT_SENT] = False


def render_header() -> None:
    """Sayfa başlığını ve alt bilgilerini HTML/CSS kart yapısı ile ekrana basar."""
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


def validate_form(room_number: str, description: str) -> str | None:
    """
    Form girişlerini doğrular. 
    Hata varsa hata mesajını döner, her şey doğruysa None döner.
    """
    if not room_number.strip():
        return "Oda numarası boş bırakılamaz."
    if not description.strip():
        return "Arıza açıklaması boş bırakılamaz."
    if len(description.strip()) < 10:
        return "Arıza açıklaması en az 10 karakter olmalıdır."
    return None


def render_form(student_number: str) -> None:
    """Arıza bildirim formunu ve buton mantığını oluşturur."""
    st.markdown('<div class="form-shell">', unsafe_allow_html=True)

    # Oda No Giriş Alanı
    st.markdown('<div class="field-label">🚪 Oda No</div>', unsafe_allow_html=True)
    room_number = st.text_input(
        "Oda No",
        label_visibility="collapsed",
        placeholder="Oda numaranızı girin",
        max_chars=10,
    )

    # Arıza Detay Giriş Alanı
    st.markdown('<div class="field-label">📝 Arıza Açıklama</div>', unsafe_allow_html=True)
    description = st.text_area(
        "Arıza Açıklama",
        label_visibility="collapsed",
        placeholder="Arızayı detaylı açıklayın.",
    )

    col1, col2 = st.columns(2)

    with col1:
        # 'Bildirimi Gönder' butonuna basıldığında tetiklenen ana mantık
        if st.button("Bildirimi Gönder", use_container_width=True):
            error_message = validate_form(room_number, description)
            
            if error_message:
                st.error(error_message) # Form doğrulama hatası varsa göster
            else:
                # Form geçerli ise API'ye POST isteği atılır
                with st.spinner("Bildiriminiz FastAPI üzerinden iletiliyor..."):
                    # Artık öğrenci numarasını API'nin beklediği gibi 'ogrenci_no' parametresiyle gönderiyoruz
                    result = send_fault_report(
                        baslik="Arıza Bildirimi", # Başlığı daha sade tutabilirsin
                        detay=description, 
                        oda_no=room_number,
                        ogrenci_no=student_number # İŞTE KRİTİK EKLENTİ BURASI!
                    )
                
                # API'den gelen yanıta göre UI yönlendirmesi yapılır
                if result["status"] == "success":
                    st.session_state[SESSION_FAULT_SENT] = True
                    st.rerun() # Başarı ekranına geçmek için sayfayı yenile
                else:
                    # Backend tarafında veya bağlantıda bir sorun oluşursa kullanıcıyı bilgilendir
                    st.error(f"⚠️ API Hatası: {result.get('message', 'Sunucuya ulaşılamadı.')}")

    with col2:
        # Kullanıcıyı bir önceki panele geri döndüren navigasyon butonu
        if st.button("Panele Dön", use_container_width=True):
            st.switch_page(STUDENT_PANEL_PAGE)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            Oluşturduğunuz arıza kaydı personel paneli üzerinden takip edilebilir.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success() -> None:
    """Arıza bildirimi başarıyla API'ye ulaştığında gösterilen onay ekranı."""
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
            st.switch_page(STUDENT_PANEL_PAGE)

    with col2:
        # Kullanıcının yeni bir bildirim daha yapabilmesi için durumu sıfırlar
        if st.button("➕ Yeni Bildirim", use_container_width=True):
            st.session_state[SESSION_FAULT_SENT] = False
            st.rerun()


def main() -> None:
    """Sayfanın ana giriş noktası ve yaşam döngüsü yönetimi."""
    
    # Güvenlik Kontrolü: Giriş yapmamış kullanıcıyı login sayfasına atar
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)
    
    # Sayfa hazırlıkları
    init_page_state()
    load_student_fault_page_styles()
    render_header()

    # Aktif öğrencinin numarasını auth sisteminden çeker
    student_number = get_student_no()

    # Gönderim durumuna göre ya form ya da başarı ekranı render edilir
    if st.session_state[SESSION_FAULT_SENT]:
        render_success()
    else:
        render_form(student_number)


# Dosya doğrudan çalıştırıldığında main() fonksiyonunu çağır
if __name__ == "__main__":
    main()