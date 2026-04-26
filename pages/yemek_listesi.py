import streamlit as st

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

    st.markdown(
        """
        <style>
        .weekday-header {
            background: #dbeafe;
            color: #1e293b;
            font-weight: 900;
            text-align: center;
            border-radius: 8px;
            padding: 5px;
            margin-bottom: 5px;
            border: 1px solid #bfdbfe;
            font-size: 11px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #cbd5f5 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 5px rgba(15, 23, 42, 0.04) !important;
            background: #f8fafc !important;
            padding: 6px !important;
            min-height: 112px !important;
        }

        div[data-testid="stTextInput"] {
            width: 34px !important;
            min-width: 34px !important;
            max-width: 34px !important;
            margin: 0 0 4px 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stTextInput"] > div {
            width: 34px !important;
            min-width: 34px !important;
            max-width: 34px !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .stTextInput input {
            width: 34px !important;
            min-width: 34px !important;
            max-width: 34px !important;
            height: 22px !important;
            font-size: 10px !important;
            font-weight: 900 !important;
            color: #1e293b !important;
            background: #dbeafe !important;
            border-radius: 6px !important;
            border: 1px solid #93c5fd !important;
            text-align: center !important;
            padding: 0 !important;
        }

        div[data-testid="stTextArea"] {
            margin: 0 !important;
            padding: 0 !important;
        }

        .stTextArea textarea {
            width: 100% !important;
            font-size: 10px !important;
            padding: 5px !important;
            border-radius: 6px !important;
            border: 1px solid #cbd5e1 !important;
            min-height: 70px !important;
            margin: 0 !important;
        }

        .stTextArea textarea:focus,
        .stTextInput input:focus {
            border: 1px solid #3b82f6 !important;
            box-shadow: 0 0 0 1px #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"Seçili Ay: {selected_month}")

    weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    header_cols = st.columns(7, gap="small")

    for i, day_name in enumerate(weekdays):
        with header_cols[i]:
            st.markdown(
                f'<div class="weekday-header">{day_name}</div>',
                unsafe_allow_html=True,
            )

    monthly_menu = st.session_state[MONTHLY_MENU_SESSION_KEY][selected_month]
    day_labels = st.session_state[MONTHLY_DAY_LABELS_KEY][selected_month]

    box_number = 1

    for _ in range(5):
        cols = st.columns(7, gap="small")

        for col in cols:
            with col:
                with st.container(border=True):
                    key = str(box_number)
                    day_labels[key] = st.text_input(
                        "",
                        value=day_labels.get(key, key),
                        key=f"day_label_{selected_month}_{box_number}",
                        label_visibility="collapsed",
                    )

                    monthly_menu[key] = st.text_area(
                        "",
                        value=monthly_menu.get(key, ""),
                        placeholder="Menü...",
                        key=f"food_day_{selected_month}_{box_number}",
                        label_visibility="collapsed",
                    )

                box_number += 1

    st.session_state[MONTHLY_MENU_SESSION_KEY][selected_month] = monthly_menu
    st.session_state[MONTHLY_DAY_LABELS_KEY][selected_month] = day_labels

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💾 Aylık Menüyü Kaydet", type="primary", use_container_width=True):
        res = save_monthly_meal_menu(st.session_state[MONTHLY_MENU_SESSION_KEY])
        if res.get("status") == "success":
            st.success(f"{selected_month} ayı yemek menüsü kaydedildi.")
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