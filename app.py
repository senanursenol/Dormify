import requests
import streamlit as st
from streamlit_lottie import st_lottie

from core.constants import (
    LOGIN_SELECTION_PAGE,
    SESSION_ANNOUNCEMENTS,
    SESSION_MEAL_MENU,
)
from core.styles import load_landing_styles
from core.ui import render_logo

from services.api_service import get_announcements, get_meal_menu


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
    except Exception:
        st.session_state[SESSION_ANNOUNCEMENTS] = st.session_state.get(SESSION_ANNOUNCEMENTS, [])
        st.session_state[SESSION_MEAL_MENU] = st.session_state.get(SESSION_MEAL_MENU, "Menü yüklenemedi.")


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
    st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">📢 Güncel Bilgilendirmeler</h3>', unsafe_allow_html=True)

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


# ----------- MODAL -----------
@st.dialog("📅 Aylık Yemek Menüsü", width="large")
def render_monthly_menu_modal() -> None:
    current_menu = st.session_state.get(SESSION_MEAL_MENU, "Aylık yemek menüsü henüz yüklenmedi.")
    st.markdown(
        f"""
        <div style="
            max-height: 500px;
            overflow-y: auto;
            padding: 20px 12px;
            color:#475569;
            font-size:16px;
            text-align:center;
        ">
            {current_menu}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_menu_card() -> None:
    st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">🍴 Bugün Ne Var?</h3>', unsafe_allow_html=True)

    current_menu = st.session_state.get(SESSION_MEAL_MENU, "Menü bilgisi yüklenemedi.")

    st.markdown(
        f"""
        <div class="modern-menu-card">
            <div style="
                text-align:center;
                color:#475569;
                font-size:15px;
                padding:20px 12px;
            ">
                {current_menu}
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