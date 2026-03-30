import streamlit as st
from typing import Dict

from core.auth import get_student_no, redirect_if_not_logged_in
from core.constants import (
    ROLE_STUDENT,
    STATUS_PENDING,
    STUDENT_LOGIN_PAGE,
    STUDENT_PANEL_PAGE,
)
from core.styles import load_student_notifications_page_styles

from services.api_service import (
    get_student_faults,   # API'den öğrenciye özel arızaları çeken fonksiyon
    update_fault_api      # İptal işlemi için API'yi kullanacağız
)
from services.fault_service import get_status_label, get_status_counts


def render_back_button() -> None:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Ana Panele Dön"):
        st.switch_page(STUDENT_PANEL_PAGE)
    st.markdown("</div>", unsafe_allow_html=True)


def render_stats(pending_count: int, solved_count: int, total_count: int) -> None:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">⏳</div>
                <div class="stat-number">{pending_count}</div>
                <div class="stat-label">Beklemede</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-number">{solved_count}</div>
                <div class="stat-label">Çözüldü</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-number">{total_count}</div>
                <div class="stat-label">Toplam</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>Bildiriminiz bulunmuyor</h3>
            <p>Henüz arıza bildirimi oluşturmadınız.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_fault_card(index: int, fault: Dict) -> None:
    # 1. Veritabanından gelen ham Türkçe kelimeyi alıyoruz
    db_durum = fault.get("durum", "Beklemede")

    # 2. CSS renklerinin (yeşil/kırmızı) çalışması için İngilizce sistem kodlarına çeviriyoruz
    if db_durum == "Çözüldü":
        status = "solved"
        status_label = "Çözüldü"
    elif db_durum == "İptal Edildi":
        status = "cancelled"
        status_label = "İptal Edildi"
    else:
        status = "pending"
        status_label = "Beklemede"

    # Kartın rengi (status) ve ekranda yazacak yazı (status_label) artık doğru!
    st.markdown(f'<div class="notice-card {status}">', unsafe_allow_html=True)

    col_left, col_right = st.columns([4, 1.2])

    with col_left:
        st.markdown(
            f'<div class="notice-title">🚪 {fault.get("oda_no", "-")} No\'lu Oda</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="notice-meta">📅 {fault.get("tarih", "-")} &nbsp;&nbsp; 👤 {fault.get("ogrenci_no", "-")}</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f'<div class="badge {status}">{status_label}</div>',
            unsafe_allow_html=True,
        )

    aciklama_metni = fault.get("aciklama") or fault.get("detay") or "Açıklama belirtilmedi."
    st.markdown(
        f'<div class="notice-desc">{aciklama_metni}</div>',
        unsafe_allow_html=True,
    )

    # İptal butonu sadece "Beklemede" (pending) durumundayken görünsün
    if status == "pending" and fault.get("id"):
        st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
        if st.button("✖ İptal", key=f"iptal_{index}", use_container_width=False):
            from services.api_service import update_fault_api
            res = update_fault_api(fault["id"], "İptal Edildi")
            if res.get("status") == "success":
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)   


def render_fault_list(faults: list[Dict]) -> None:
    st.markdown('<div class="list-container">', unsafe_allow_html=True)

    if not faults:
        render_empty_state()
    else:
        for index, fault in enumerate(faults):
            render_fault_card(index, fault)

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)
    # init_fault_state() -> Artık API kullandığımız için buna gerek kalmayabilir
    load_student_notifications_page_styles()

    student_number = get_student_no()
    
    # ARTIK VERİYİ DOĞRUDAN API'DEN ÇEKİYORUZ
    faults = get_student_faults(student_number) 
    
    # İstatistikleri hesapla
    pending_count, solved_count, total_count = get_status_counts(faults)

    render_back_button()
    render_stats(pending_count, solved_count, total_count)
    render_fault_list(faults)

main()