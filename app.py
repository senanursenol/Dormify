import requests
import streamlit as st
import calendar
from streamlit_lottie import st_lottie
from datetime import datetime

from core.constants import (
    LOGIN_SELECTION_PAGE,
    SESSION_ANNOUNCEMENTS,
    SESSION_MEAL_MENU,
)
from core.styles import load_landing_styles
from core.ui import render_logo

from services.api_service import get_announcements, get_meal_menu, get_monthly_meal_menu, get_breakfast_menu, get_monthly_breakfast_menu

# Kahvaltı fonksiyonları api_service.py içinde varsa kullanılır.
# Yoksa kod hata vermesin diye default değer döndürür.
try:
    from services.api_service import get_monthly_breakfast_menu
except ImportError:
    def get_monthly_breakfast_menu():
        return {}


def load_lottieurl(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def sync_data_from_api() -> None:
    try:
        st.session_state[SESSION_ANNOUNCEMENTS] = get_announcements()
        st.session_state[SESSION_MEAL_MENU] = get_meal_menu()
        st.session_state["SESSION_BREAKFAST_MENU"] = get_breakfast_menu()
    except Exception:
        st.session_state[SESSION_ANNOUNCEMENTS] = st.session_state.get(
            SESSION_ANNOUNCEMENTS,
            []
        )
        st.session_state[SESSION_MEAL_MENU] = st.session_state.get(
            SESSION_MEAL_MENU,
            "Menü yüklenemedi."
        )
        st.session_state["SESSION_BREAKFAST_MENU"] = st.session_state.get(
            "SESSION_BREAKFAST_MENU",
            "Kahvaltı menüsü yüklenemedi."
        )


# ---------------- HEADER ----------------
def render_header() -> None:
    col_left, col_mid, col_right = st.columns([1, 6, 1])

    with col_left:
        render_logo(center=False, width=280)

    with col_right:
        st.write("##")
        if st.button("Sisteme Giriş Yap →", key="nav_btn"):
            st.switch_page(LOGIN_SELECTION_PAGE)


def render_hero(lottie_json) -> None:
    if lottie_json:
        st_lottie(lottie_json, height=350, key="main_home_anim")

    st.markdown(
        """
        <div style="text-align: center; margin-top: -20px; margin-bottom: 50px;">
            <h1 style="font-size: 3.5rem; font-weight:900; color:#1e293b; margin:0;">
                Dormify <span style="color:#3b82f6;">Portal</span>
            </h1>
            <p style="font-size: 1.2rem; color:#475569; margin-top: 15px;">
                Beylikdüzü Özel Ensar Vakfı Kız Yurdu <br>
                <b>Dijital Yönetim Platformu</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_announcements() -> None:
    st.markdown(
        '<h3 style="color:#1e293b; margin-bottom:20px;">📢 Güncel Bilgilendirmeler</h3>',
        unsafe_allow_html=True,
    )

    duyurular = st.session_state.get(SESSION_ANNOUNCEMENTS, [])

    if not duyurular:
        st.info("Şu an aktif bir duyuru bulunmamaktadır.")
        return

    for duyuru in duyurular:
        st.markdown(
            f"""
            <div class="custom-card" style="border-left: 8px solid {duyuru.get('renk', '#3b82f6')};">
                <h4>{duyuru.get('baslik')}</h4>
                <p>{duyuru.get('icerik')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ----------- AYLIK MENÜ MODALI (POP-UP) -----------
@st.dialog("📅 Bu Ayın Yemek Takvimi", width="large")
def render_monthly_menu_modal() -> None:
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    MONTHS = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    current_month_name = MONTHS[current_month - 1]

    st.markdown(
        """
        <style>
        .cal-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-top: 15px;
        }

        .cal-th {
            background-color: #f8fafc;
            color: #1e293b;
            padding: 10px;
            text-align: center;
            border: 1px solid #cbd5e1;
            font-weight: 800;
            font-size: 14px;
        }

        .cal-td {
            border: 1px solid #cbd5e1;
            vertical-align: top;
            height: 120px;
            padding: 8px;
            background-color: white;
            overflow: hidden;
        }

        .cal-td-empty {
            background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
        }

        .cal-today {
            background-color: #eff6ff;
            border: 2px solid #3b82f6;
            box-shadow: inset 0 0 5px rgba(59,130,246,0.2);
        }

        .day-num {
            font-weight: 900;
            color: #3b82f6;
            font-size: 14px;
            margin-bottom: 6px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3px;
        }

        .meal-desc {
            font-size: 11px;
            color: #475569;
            line-height: 1.45;
            word-wrap: break-word;
        }

        div[data-testid="stTabs"] button {
            font-weight: 700;
            font-size: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def create_calendar_html(month_data: dict) -> str:
        cal_matrix = calendar.monthcalendar(current_year, current_month)
        weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

        html = '<table class="cal-table"><tr>'

        for w in weekdays:
            html += f"<th class='cal-th'>{w}</th>"
        html += "</tr>"

        for week in cal_matrix:
            html += "<tr>"

            for day in week:
                if day == 0:
                    html += "<td class='cal-td-empty'></td>"
                else:
                    menu_text = month_data.get(str(day), "").strip()
                    menu_text = menu_text.replace("\n", "<br>")

                    is_today = day == now.day
                    td_class = "cal-td cal-today" if is_today else "cal-td"
                    star = "⭐ " if is_today else ""

                    html += (
                        f"<td class='{td_class}'>"
                        f"<div class='day-num'>{star}{day}</div>"
                        f"<div class='meal-desc'>{menu_text}</div>"
                        f"</td>"
                    )

            html += "</tr>"

        html += "</table>"
        return html

    # Solda Kahvaltı, sağda Akşam Yemeği
    tab_kahvalti, tab_aksam = st.tabs(["☕ Kahvaltı", "🍽️ Akşam Yemeği"])

    with tab_kahvalti:
        with st.spinner("Kahvaltı menüsü yükleniyor..."):
            all_breakfast_data = get_monthly_breakfast_menu()
            breakfast_month_data = all_breakfast_data.get(current_month_name, {})

        if not breakfast_month_data:
            st.info("Bu ay için kahvaltı menüsü girilmemiştir.")
        else:
            breakfast_html = create_calendar_html(breakfast_month_data)
            st.markdown(breakfast_html, unsafe_allow_html=True)

    with tab_aksam:
        with st.spinner("Akşam yemeği menüsü yükleniyor..."):
            all_dinner_data = get_monthly_meal_menu()
            dinner_month_data = all_dinner_data.get(current_month_name, {})

        if not dinner_month_data:
            st.info("Bu ay için akşam yemeği menüsü girilmemiştir.")
        else:
            dinner_html = create_calendar_html(dinner_month_data)
            st.markdown(dinner_html, unsafe_allow_html=True)


def format_menu_items(menu_text: str) -> str:
    if not isinstance(menu_text, str):
        return (
            "<div class='menu-item'>"
            "<span class='meal-emoji'>🌟</span>"
            "<span>Menü bilgisi yüklenemedi.</span>"
            "</div>"
        )

    cleaned_menu = menu_text.replace("\n", ",")
    menu_items = [item.strip() for item in cleaned_menu.split(",") if item.strip()]

    if not menu_items:
        return (
            "<div class='menu-item'>"
            "<span class='meal-emoji'>🌟</span>"
            "<span>Menü bilgisi bulunamadı.</span>"
            "</div>"
        )

    formatted_menu = "".join(
        [
            f"<div class='menu-item'><span class='meal-emoji'>🌟</span><span>{item}</span></div>"
            for item in menu_items
        ]
    )

    return formatted_menu


def render_menu_card() -> None:
    st.markdown(
        '<h3 style="color:#1e293b; margin-bottom:20px;">🍴 Bugün Ne Var?</h3>',
        unsafe_allow_html=True,
    )

    # Ana sayfada ekranı boğmayan küçük seçim alanı
    menu_type = st.radio(
        label="Menü türü seçin",
        options=["☕ Kahvaltı", "🍽️ Akşam"],
        horizontal=True,
        label_visibility="collapsed",
        key="today_menu_type",
    )

    if menu_type == "☕ Kahvaltı":
        current_menu = st.session_state.get(
            "SESSION_BREAKFAST_MENU",
            "Kahvaltı menüsü yüklenemedi."
        )
        card_title = "Kahvaltı"
    else:
        current_menu = st.session_state.get(
            SESSION_MEAL_MENU,
            "Akşam yemeği menüsü yüklenemedi."
        )
        card_title = "Akşam Yemeği"

    formatted_menu = format_menu_items(current_menu)

    st.markdown(
f"""
<style>
div[role="radiogroup"] {{
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: -8px;
    margin-bottom: 12px;
}}

div[role="radiogroup"] label {{
    background-color: rgba(255, 255, 255, 0.75);
    border-radius: 999px;
    padding: 5px 10px;
    border: 1px solid rgba(148, 163, 184, 0.35);
}}

.menu-card-title {{
    text-align: center;
    color: #1e293b;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 6px;
}}

.menu-list {{
    text-align: left;
    color: #475569;
    font-size: 15px;
    line-height: 1.65;
    padding: 8px 36px 8px 36px;
}}

.menu-item {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
    font-weight: 600;
}}

.meal-emoji {{
    min-width: 24px;
    display: inline-block;
    text-align: center;
}}

.afiyet-text {{
    text-align: center;
    color: #00853e;
    font-weight: 900;
    letter-spacing: 2px;
    font-size: 13px;
    margin-top: 20px;
}}
</style>

<div class="modern-menu-card">
    <div class="menu-card-title">{card_title}</div>
    <div class="menu-list">
        {formatted_menu}
    </div>
    <div class="afiyet-text">AFİYET OLSUN!</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.button("📅 Aylık Menü", use_container_width=True, key="btn_aylik_menu"):
        render_monthly_menu_modal()

    if st.button("🔧 Arıza Bildirimi", use_container_width=True, key="btn_ariza"):
        st.info("Lütfen önce giriş yapın.")


def main() -> None:
    st.set_page_config(
        page_title="Dormify | Ensar Vakfı",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    load_landing_styles()
    sync_data_from_api()

    lottie_home_json = load_lottieurl(
        "https://lottie.host/f5b2c1e5-8c7a-4f9e-9b4e-5d3f2c1e8b9a/x9Y2K1vB8m.json"
    )

    render_header()
    render_hero(lottie_home_json)

    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2.5, 1], gap="large")

    with col_main:
        render_announcements()

    with col_side:
        render_menu_card()

    st.markdown(
        "<center><p style='color:#94a3b8; padding:60px; font-size:12px;'>© 2026 Dormify | Ensar Vakfı</p></center>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()