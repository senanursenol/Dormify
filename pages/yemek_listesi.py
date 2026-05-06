import streamlit as st
import calendar
from datetime import datetime
from core.auth import redirect_if_not_logged_in
from core.constants import ROLE_STAFF, STAFF_LOGIN_PAGE
from core.styles import load_student_panel_page_styles
from services.api_service import get_monthly_meal_menu, save_monthly_meal_menu


MONTHLY_DINNER_MENU_SESSION_KEY = "monthly_food_calendar"
MONTHLY_BREAKFAST_MENU_SESSION_KEY = "monthly_breakfast_calendar"
MONTHLY_DAY_LABELS_KEY = "monthly_food_day_labels"
MONTHLY_SELECTED_MONTH_KEY = "monthly_selected_month"
MONTHLY_SELECTED_MEAL_TYPE_KEY = "monthly_selected_meal_type"
MONTHLY_MENU_LOADED_KEY = "monthly_menu_loaded"

MONTHS = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]

MEAL_TYPES = ["Kahvaltı", "Akşam Yemeği"]


def render_back() -> None:
    if st.button("← Personel Paneline Dön"):
        st.switch_page("pages/personel_panel.py")


def create_empty_monthly_menu() -> dict:
    return {
        month: {str(day): "" for day in range(1, 36)}
        for month in MONTHS
    }


def init_monthly_menu_state() -> None:
    if MONTHLY_SELECTED_MONTH_KEY not in st.session_state:
        st.session_state[MONTHLY_SELECTED_MONTH_KEY] = "Ocak"

    if MONTHLY_SELECTED_MEAL_TYPE_KEY not in st.session_state:
        st.session_state[MONTHLY_SELECTED_MEAL_TYPE_KEY] = "Akşam Yemeği"

    # Akşam yemeği eski database yapısıyla aynı tutuluyor
    if MONTHLY_DINNER_MENU_SESSION_KEY not in st.session_state:
        st.session_state[MONTHLY_DINNER_MENU_SESSION_KEY] = create_empty_monthly_menu()

    # Kahvaltı şimdilik database'e bağlı değil, sadece session'da tutuluyor
    if MONTHLY_BREAKFAST_MENU_SESSION_KEY not in st.session_state:
        st.session_state[MONTHLY_BREAKFAST_MENU_SESSION_KEY] = create_empty_monthly_menu()

    if MONTHLY_DAY_LABELS_KEY not in st.session_state:
        st.session_state[MONTHLY_DAY_LABELS_KEY] = {
            month: {str(day): str(day) for day in range(1, 36)}
            for month in MONTHS
        }

    if MONTHLY_MENU_LOADED_KEY not in st.session_state:
        st.session_state[MONTHLY_MENU_LOADED_KEY] = False


def sync_monthly_menu_from_api() -> None:
    """
    Sadece akşam yemeği database'den çekiliyor.
    Kahvaltı henüz database'e bağlı olmadığı için burada API'den alınmıyor.
    """
    if st.session_state.get(MONTHLY_MENU_LOADED_KEY):
        return

    menu_data = get_monthly_meal_menu()

    if isinstance(menu_data, dict) and menu_data:
        st.session_state[MONTHLY_DINNER_MENU_SESSION_KEY] = menu_data

    st.session_state[MONTHLY_MENU_LOADED_KEY] = True


def render_top_controls() -> tuple[str, str]:
    col_left, col_right = st.columns([5, 1.5])

    with col_left:
        st.title("🍽️ Aylık Yemek Menüsü Takvimi")

        selected_meal_type = st.radio(
            "Menü Türü Seç",
            MEAL_TYPES,
            horizontal=True,
            key=MONTHLY_SELECTED_MEAL_TYPE_KEY,
        )

    with col_right:
        selected_month = st.selectbox(
            "Ay Seç",
            MONTHS,
            index=MONTHS.index(st.session_state[MONTHLY_SELECTED_MONTH_KEY]),
            key=MONTHLY_SELECTED_MONTH_KEY,
        )

    return selected_month, selected_meal_type


def get_active_menu(selected_meal_type: str, selected_month: str) -> dict:
    if selected_meal_type == "Kahvaltı":
        return st.session_state[MONTHLY_BREAKFAST_MENU_SESSION_KEY][selected_month]

    return st.session_state[MONTHLY_DINNER_MENU_SESSION_KEY][selected_month]


def update_active_menu(selected_meal_type: str, selected_month: str, monthly_menu: dict) -> None:
    if selected_meal_type == "Kahvaltı":
        st.session_state[MONTHLY_BREAKFAST_MENU_SESSION_KEY][selected_month] = monthly_menu
    else:
        st.session_state[MONTHLY_DINNER_MENU_SESSION_KEY][selected_month] = monthly_menu


def render_monthly_food_calendar() -> None:
    selected_month, selected_meal_type = render_top_controls()

    current_year = datetime.now().year
    month_index = MONTHS.index(selected_month) + 1

    st.caption(f"Seçili Ay: {selected_month} {current_year}")
    st.caption(f"Düzenlenen Menü: {selected_meal_type}")

    weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    header_cols = st.columns(7, gap="small")

    for i, day_name in enumerate(weekdays):
        with header_cols[i]:
            st.markdown(
                f'<div class="weekday-header">{day_name}</div>',
                unsafe_allow_html=True,
            )

    month_matrix = calendar.monthcalendar(current_year, month_index)

    monthly_menu = get_active_menu(selected_meal_type, selected_month)

    for week in month_matrix:
        cols = st.columns(7, gap="small")

        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown(
                        '<div style="min-height: 112px;"></div>',
                        unsafe_allow_html=True
                    )
                else:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div style="
                                text-align: center;
                                font-weight: 900;
                                font-size: 12px;
                                margin-bottom: 5px;
                                color: #1e293b;
                                background: #dbeafe;
                                border-radius: 6px;
                            ">
                                {day}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        key_day = str(day)

                        if selected_meal_type == "Kahvaltı":
                            placeholder_text = "Kahvaltı menüsü..."
                            textarea_key = f"breakfast_day_{selected_month}_{day}"
                        else:
                            placeholder_text = "Akşam yemeği menüsü..."
                            textarea_key = f"dinner_day_{selected_month}_{day}"

                        monthly_menu[key_day] = st.text_area(
                            "",
                            value=monthly_menu.get(key_day, ""),
                            placeholder=placeholder_text,
                            key=textarea_key,
                            label_visibility="collapsed",
                        )

    update_active_menu(selected_meal_type, selected_month, monthly_menu)

    st.markdown("<br>", unsafe_allow_html=True)

    if selected_meal_type == "Akşam Yemeği":
        if st.button("💾 Akşam Yemeği Menüsünü Kaydet", type="primary", use_container_width=True):
            payload = {
                "yil": current_year,
                "ay": selected_month,
                "gunler": st.session_state[MONTHLY_DINNER_MENU_SESSION_KEY][selected_month]
            }

            res = save_monthly_meal_menu(payload)

            if res.get("status") == "success":
                st.success(f"{selected_month} {current_year} akşam yemeği menüsü başarıyla kaydedildi!")
            else:
                st.error(res.get("message", "Aylık yemek menüsü kaydedilirken bir hata oluştu."))

    else:
        st.info("Kahvaltı menüsü şu an sadece ekranda düzenlenir. Database kaydı daha sonra eklenecek.")

        if st.button("✅ Kahvaltı Menüsünü Kaydet", use_container_width=True):
            st.session_state[MONTHLY_BREAKFAST_MENU_SESSION_KEY][selected_month] = monthly_menu
            st.success(f"{selected_month} {current_year} kahvaltı menüsü kaydedildi.")


def main() -> None:
    redirect_if_not_logged_in(ROLE_STAFF, STAFF_LOGIN_PAGE)

    load_student_panel_page_styles()
    init_monthly_menu_state()
    sync_monthly_menu_from_api()

    render_back()
    render_monthly_food_calendar()


if __name__ == "__main__":
    main()