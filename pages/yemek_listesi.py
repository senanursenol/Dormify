import streamlit as st
import calendar
from datetime import datetime
from core.auth import redirect_if_not_logged_in
from core.constants import ROLE_STAFF, STAFF_LOGIN_PAGE
from core.styles import load_student_panel_page_styles
from services.api_service import get_monthly_meal_menu, save_monthly_meal_menu


MONTHLY_MENU_SESSION_KEY = "monthly_food_calendar"
MONTHLY_DAY_LABELS_KEY = "monthly_food_day_labels"
MONTHLY_SELECTED_MONTH_KEY = "monthly_selected_month"
MONTHLY_MENU_LOADED_KEY = "monthly_menu_loaded"

MONTHS = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]


def render_back() -> None:
    if st.button("← Personel Paneline Dön"):
        st.switch_page("pages/personel_panel.py")


def init_monthly_menu_state() -> None:
    if MONTHLY_SELECTED_MONTH_KEY not in st.session_state:
        st.session_state[MONTHLY_SELECTED_MONTH_KEY] = "Ocak"

    if MONTHLY_MENU_SESSION_KEY not in st.session_state:
        st.session_state[MONTHLY_MENU_SESSION_KEY] = {
            month: {str(day): "" for day in range(1, 36)}
            for month in MONTHS
        }

    if MONTHLY_DAY_LABELS_KEY not in st.session_state:
        st.session_state[MONTHLY_DAY_LABELS_KEY] = {
            month: {str(day): str(day) for day in range(1, 36)}
            for month in MONTHS
        }

    if MONTHLY_MENU_LOADED_KEY not in st.session_state:
        st.session_state[MONTHLY_MENU_LOADED_KEY] = False


def sync_monthly_menu_from_api() -> None:
    if st.session_state.get(MONTHLY_MENU_LOADED_KEY):
        return

    menu_data = get_monthly_meal_menu()
    if isinstance(menu_data, dict) and menu_data:
        st.session_state[MONTHLY_MENU_SESSION_KEY] = menu_data
    st.session_state[MONTHLY_MENU_LOADED_KEY] = True


def render_month_selector() -> str:
    col_left, col_right = st.columns([5, 1.5])

    with col_left:
        st.title("🍽️ Aylık Yemek Menüsü Takvimi")

    with col_right:
        selected_month = st.selectbox(
            "Ay Seç",
            MONTHS,
            index=MONTHS.index(st.session_state[MONTHLY_SELECTED_MONTH_KEY]),
            key=MONTHLY_SELECTED_MONTH_KEY,
        )

    return selected_month


def render_monthly_food_calendar() -> None:
    selected_month = render_month_selector()
    
    # Gerçek takvim mantığı için mevcut yılı alıyoruz
    current_year = datetime.now().year
    month_index = MONTHS.index(selected_month) + 1 # Seçilen ayın numarasını (1-12) buluruz

    # --- CSS KODLARINIZ BURADA AYNEN KALSIN (Çok uzun olduğu için buraya yazmıyorum, arkadaşının yazdığı <style> bloğunu buraya koy) ---
    # st.markdown(""" <style> ... </style> """, unsafe_allow_html=True)
    
    st.caption(f"Seçili Ay: {selected_month} {current_year}")

    weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    header_cols = st.columns(7, gap="small")

    for i, day_name in enumerate(weekdays):
        with header_cols[i]:
            st.markdown(
                f'<div class="weekday-header">{day_name}</div>',
                unsafe_allow_html=True,
            )

    # Python'un Sihirli Takvim Matrisi!
    # Bize haftaları liste olarak verir. Ayın dışındaki günleri 0 yapar.
    month_matrix = calendar.monthcalendar(current_year, month_index)

    monthly_menu = st.session_state[MONTHLY_MENU_SESSION_KEY][selected_month]

    # Matristeki her hafta için bir satır oluştur
    for week in month_matrix:
        cols = st.columns(7, gap="small")
        
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    # Bu kutu ayın dışında kalıyor, o yüzden görünmez boş bir alan çiz
                    st.markdown('<div style="min-height: 112px;"></div>', unsafe_allow_html=True)
                else:
                    # Gerçek bir gün, kutuyu ve metin alanını çiz!
                    with st.container(border=True):
                        # Gün numarasını değiştirmelerine gerek yok, sabit yazıyoruz
                        st.markdown(f'<div style="text-align: center; font-weight: 900; font-size: 12px; margin-bottom: 5px; color: #1e293b; background: #dbeafe; border-radius: 6px;">{day}</div>', unsafe_allow_html=True)

                        key_day = str(day)
                        monthly_menu[key_day] = st.text_area(
                            "",
                            value=monthly_menu.get(key_day, ""),
                            placeholder="Menü...",
                            key=f"food_day_{selected_month}_{day}",
                            label_visibility="collapsed",
                        )

    st.session_state[MONTHLY_MENU_SESSION_KEY][selected_month] = monthly_menu
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 Aylık Menüyü Kaydet", type="primary", use_container_width=True):
        # Tüm yılı değil, sadece işlem yapılan Yılı, Ayı ve Günleri API'ye paketliyoruz!
        payload = {
            "yil": current_year,
            "ay": selected_month,
            "gunler": st.session_state[MONTHLY_MENU_SESSION_KEY][selected_month]
        }
        res = save_monthly_meal_menu(payload)
        
        if res.get("status") == "success":
            st.success(f"{selected_month} {current_year} menüsü başarıyla kaydedildi!")
        else:
            st.error(res.get("message", "Aylık yemek menüsü kaydedilirken bir hata oluştu."))
def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)

    load_student_panel_page_styles()
    init_monthly_menu_state()
    sync_monthly_menu_from_api()

    render_back()
    render_monthly_food_calendar()


if __name__ == "__main__":
    main()