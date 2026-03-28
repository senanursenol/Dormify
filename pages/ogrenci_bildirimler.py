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
from services.fault_service import (
    cancel_fault_by_id,
    get_status_counts,
    get_status_label,
    get_student_faults,
    init_fault_state,
)


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
    status = fault.get("durum", STATUS_PENDING)
    status_label = get_status_label(status)

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

    st.markdown(
        f'<div class="notice-desc">{fault.get("aciklama", "")}</div>',
        unsafe_allow_html=True,
    )

    if status == STATUS_PENDING and fault.get("id"):
        st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
        if st.button("✖ İptal", key=f"iptal_{index}", use_container_width=False):
            cancel_fault_by_id(fault["id"])
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
    init_fault_state()
    load_student_notifications_page_styles()

    student_number = get_student_no()
    faults = get_student_faults(student_number)
    pending_count, solved_count, total_count = get_status_counts(faults)

    render_back_button()
    render_stats(pending_count, solved_count, total_count)
    render_fault_list(faults)


main()