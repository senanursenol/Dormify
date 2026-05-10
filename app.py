import requests
import streamlit as st
import calendar
import base64
from streamlit_lottie import st_lottie
from datetime import datetime

# --- CORE VE SERVİS MODÜLLERİ ---
from core.constants import (
    LOGIN_SELECTION_PAGE,
    SESSION_ANNOUNCEMENTS,
    SESSION_MEAL_MENU,
)
from core.styles import load_landing_styles
from core.ui import render_logo

from services.api_service import (
    get_announcements, 
    get_meal_menu, 
    get_monthly_meal_menu, 
    get_breakfast_menu, 
    get_monthly_breakfast_menu
)

# --- YARDIMCI FONKSİYONLAR ---

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
        st.session_state[SESSION_ANNOUNCEMENTS] = st.session_state.get(SESSION_ANNOUNCEMENTS, [])
        st.session_state[SESSION_MEAL_MENU] = st.session_state.get(SESSION_MEAL_MENU, "Menü yüklenemedi.")
        st.session_state["SESSION_BREAKFAST_MENU"] = st.session_state.get("SESSION_BREAKFAST_MENU", "Kahvaltı menüsü yüklenemedi.")

# --- UI BİLEŞENLERİ ---

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
    """Arel Üniversitesi Tarzı: Üstte Otomatik Slider, Altta Bilgi Kartları."""
    st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">📢 Güncel Bilgilendirmeler</h3>', unsafe_allow_html=True)
    duyurular = st.session_state.get(SESSION_ANNOUNCEMENTS, [])

    if not duyurular:
        st.info("Şu an aktif bir duyuru bulunmamaktadır.")
        return

    # --- BÖLÜM 1: ÖNE ÇIKAN SLIDER (İlk 3 Duyuru) ---
    slider_data = duyurular[:3]
    slides_html = ""
    dots_html = ""
    
    for i, duyuru in enumerate(slider_data):
        gorsel_verisi = duyuru.get('gorsel', '')
        # Base64 kontrolü ve formatlama
        src = f"data:image/jpeg;base64,{gorsel_verisi}" if (gorsel_verisi and len(gorsel_verisi) > 100) else gorsel_verisi
        
        img_tag = f'<img src="{src}" class="slider-img">' if gorsel_verisi else f'<div class="slider-fallback" style="background:{duyuru.get("renk", "#3b82f6")}">📢</div>'

        slides_html += f"""
        <div class="mySlides fade">
            <div class="slider-box">
                {img_tag}
                <div class="slider-desc">
                    <h4>{duyuru.get('baslik')}</h4>
                    <p>{duyuru.get('icerik')[:150]}...</p>
                </div>
            </div>
        </div>
        """
        dots_html += f'<span class="dot" onclick="currentSlide({i+1})"></span>'

    st.markdown(f"""
        <style>
        .slideshow-container {{ max-width: 100%; position: relative; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .slider-box {{ position: relative; height: 420px; }}
        .slider-img {{ width: 100%; height: 420px; object-fit: cover; display: block; }}
        .slider-fallback {{ width: 100%; height: 420px; display:flex; align-items:center; justify-content:center; font-size:60px; color:white; }}
        .slider-desc {{ 
            position: absolute; bottom: 0; left: 0; right: 0; 
            background: linear-gradient(transparent, rgba(0,0,0,0.9)); 
            color: white; padding: 60px 25px 25px 25px; text-align: left;
        }}
        .slider-desc h4 {{ margin: 0; font-size: 26px; color: white !important; font-weight: 800; }}
        .slider-desc p {{ margin: 10px 0 0 0; font-size: 15px; opacity: 0.9; line-height: 1.4; }}
        .dot {{ cursor: pointer; height: 12px; width: 12px; margin: 0 5px; background-color: #cbd5e1; border-radius: 50%; display: inline-block; transition: 0.3s; }}
        .active {{ background-color: #3b82f6; width: 30px; border-radius: 10px; }}
        .fade {{ animation: fade 1.5s; }}
        @keyframes fade {{ from {{opacity: .4}} to {{opacity: 1}} }}
        </style>
        
        <div class="slideshow-container">{slides_html}</div>
        <div style="text-align:center; margin-top:15px; margin-bottom:30px;">{dots_html}</div>
        
        <script>
            let sIdx = 0;
            let timeout;
            function runSlides() {{
                let s = document.getElementsByClassName("mySlides");
                let d = document.getElementsByClassName("dot");
                if(!s.length) return;
                for(let i=0; i<s.length; i++) s[i].style.display = "none";
                sIdx++;
                if(sIdx > s.length) sIdx = 1;
                for(let i=0; i<d.length; i++) d[i].className = d[i].className.replace(" active", "");
                s[sIdx-1].style.display = "block";
                d[sIdx-1].className += " active";
                timeout = setTimeout(runSlides, 5000);
            }}
            runSlides();
        </script>
    """, unsafe_allow_html=True)

    # --- BÖLÜM 2: DİĞER DUYURULAR (Grid) ---
    if len(duyurular) > 3:
        st.markdown('<p style="font-weight:700; color:#64748b; border-bottom:2px solid #f1f5f9; padding-bottom:10px; margin-top:20px;">📌 Tüm Bilgilendirmeler</p>', unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, duyuru in enumerate(duyurular[3:]):
            with cols[idx % 2]:
                with st.container(border=True):
                    g_v = duyuru.get('gorsel', '')
                    if g_v:
                        src = f"data:image/jpeg;base64,{g_v}" if len(g_v) > 100 else g_v
                        st.image(src, use_container_width=True)
                    st.markdown(f"**{duyuru.get('baslik')}**")
                    st.caption(f"{duyuru.get('icerik')[:100]}...")
                    st.markdown(f"<small style='color:#94a3b8;'>📅 {duyuru.get('tarih')}</small>", unsafe_allow_html=True)

# ----------- YEMEK MENÜSÜ VE DİĞERLERİ -----------

@st.dialog("📅 Bu Ayın Yemek Takvimi", width="large")
def render_monthly_menu_modal() -> None:
    now = datetime.now()
    MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
    current_month_name = MONTHS[now.month - 1]

    st.markdown("""<style>.cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-top: 15px; } .cal-th { background-color: #f8fafc; color: #1e293b; padding: 10px; text-align: center; border: 1px solid #cbd5e1; font-weight: 800; font-size: 14px; } .cal-td { border: 1px solid #cbd5e1; vertical-align: top; height: 120px; padding: 8px; background-color: white; overflow: hidden; } .cal-td-empty { background-color: #f1f5f9; border: 1px solid #cbd5e1; } .cal-today { background-color: #eff6ff; border: 2px solid #3b82f6; } .day-num { font-weight: 900; color: #3b82f6; font-size: 14px; margin-bottom: 6px; border-bottom: 1px solid #e2e8f0; } .meal-desc { font-size: 11px; color: #475569; line-height: 1.45; }</style>""", unsafe_allow_html=True)

    def create_calendar_html(month_data: dict) -> str:
        cal_matrix = calendar.monthcalendar(now.year, now.month)
        weekdays = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        html = '<table class="cal-table"><tr>'
        for w in weekdays: html += f"<th class='cal-th'>{w}</th>"
        html += "</tr>"
        for week in cal_matrix:
            html += "<tr>"
            for day in week:
                if day == 0: html += "<td class='cal-td-empty'></td>"
                else:
                    menu_text = month_data.get(str(day), "").strip().replace("\n", "<br>")
                    is_today = day == now.day
                    td_class = "cal-td cal-today" if is_today else "cal-td"
                    html += f"<td class='{td_class}'><div class='day-num'>{'⭐ ' if is_today else ''}{day}</div><div class='meal-desc'>{menu_text}</div></td>"
            html += "</tr>"
        html += "</table>"
        return html

    t1, t2 = st.tabs(["☕ Kahvaltı", "🍽️ Akşam Yemeği"])
    with t1:
        data = get_monthly_breakfast_menu().get(current_month_name, {})
        st.markdown(create_calendar_html(data), unsafe_allow_html=True) if data else st.info("Veri yok.")
    with t2:
        data = get_monthly_meal_menu().get(current_month_name, {})
        st.markdown(create_calendar_html(data), unsafe_allow_html=True) if data else st.info("Veri yok.")

def format_menu_items(menu_text: str) -> str:
    if not isinstance(menu_text, str): return ""
    items = [i.strip() for i in menu_text.replace("\n", ",").split(",") if i.strip()]
    return "".join([f"<div class='menu-item'><span class='meal-emoji'>🌟</span><span>{item}</span></div>" for item in items])

def render_menu_card() -> None:
    st.markdown('<h3 style="color:#1e293b; margin-bottom:20px;">🍴 Bugün Ne Var?</h3>', unsafe_allow_html=True)
    m_type = st.radio("Seç", ["☕ Kahvaltı", "🍽️ Akşam"], horizontal=True, label_visibility="collapsed")
    key = "SESSION_BREAKFAST_MENU" if m_type == "☕ Kahvaltı" else SESSION_MEAL_MENU
    current_menu = st.session_state.get(key, "Yükleniyor...")
    
    st.markdown(f"""
        <style>
        .modern-menu-card {{ background: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; }}
        .menu-card-title {{ text-align: center; font-weight: 800; color: #1e293b; margin-bottom: 15px; }}
        .menu-item {{ display: flex; gap: 10px; margin-bottom: 8px; font-weight: 600; color: #475569; }}
        .afiyet-text {{ text-align: center; color: #00853e; font-weight: 900; margin-top: 15px; font-size: 13px; }}
        </style>
        <div class="modern-menu-card">
            <div class="menu-card-title">{'Kahvaltı' if m_type == "☕ Kahvaltı" else 'Akşam Yemeği'}</div>
            <div class="menu-list">{format_menu_items(current_menu)}</div>
            <div class="afiyet-text">AFİYET OLSUN!</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("📅 Aylık Menü", use_container_width=True): render_monthly_menu_modal()
    if st.button("🔧 Arıza Bildirimi", use_container_width=True): st.info("Lütfen giriş yapın.")

def main() -> None:
    st.set_page_config(page_title="Dormify | Ensar Vakfı", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")
    load_landing_styles()
    sync_data_from_api()
    lottie_home = load_lottieurl("https://lottie.host/f5b2c1e5-8c7a-4f9e-9b4e-5d3f2c1e8b9a/x9Y2K1vB8m.json")
    render_header()
    render_hero(lottie_home)
    col_main, col_side = st.columns([2.5, 1], gap="large")
    with col_main: render_announcements()
    with col_side: render_menu_card()
    st.markdown("<center><p style='color:#94a3b8; padding:60px; font-size:12px;'>© 2026 Dormify | Ensar Vakfı</p></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()