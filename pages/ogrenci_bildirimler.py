import streamlit as st
from typing import Dict

from core.auth import get_student_no, redirect_if_not_logged_in
from core.constants import (
    ROLE_STUDENT,
    STUDENT_LOGIN_PAGE,
    STUDENT_PANEL_PAGE,
)
from core.styles import load_student_notifications_page_styles

from services.api_service import (
    get_student_faults,
    update_fault_api
)
from services.fault_service import get_status_counts


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


def get_status_info(fault: Dict) -> tuple[str, str, str]:
    db_durum = fault.get("durum", "Beklemede")

    if db_durum == "Çözüldü":
        return "solved", "Çözüldü", "✅"
    elif db_durum == "İptal Edildi":
        return "cancelled", "İptal Edildi", "❌"
    else:
        return "pending", "Beklemede", "⏳"


def cancel_fault(fault_id: int) -> None:
    res = update_fault_api(fault_id, "İptal Edildi")
    if res.get("status") == "success":
        st.rerun()
    else:
        st.error("Bildirim iptal edilemedi.")


def delete_fault(fault_id: int) -> None:
    # Backend "Silindi" durumunu desteklemelidir.
    res = update_fault_api(fault_id, "Silindi")
    if res.get("status") == "success":
        st.rerun()
    else:
        st.error("Bildirim silinemedi. Backend'de silme desteği olmayabilir.")


def render_fault_card(index: int, fault: Dict) -> None:
    status, status_label, status_icon = get_status_info(fault)

    oda_no = fault.get("oda_no", "-")
    tarih = fault.get("tarih", "-")
    ogrenci_no = fault.get("ogrenci_no", "-")
    aciklama = fault.get("aciklama") or fault.get("detay") or "Açıklama belirtilmedi."

    with st.container(border=True):
        # ÜST SATIR
        left, right = st.columns([5, 1])

        with left:
            st.markdown(f"#### 🚪 {oda_no} No'lu Oda")
            st.caption(f"📅 {tarih}   |   👤 {ogrenci_no}")

        with right:
            if fault.get("id"):
                if st.button("✕", key=f"sil_{index}", use_container_width=True):
                    delete_fault(fault["id"])

        # AÇIKLAMA
        st.write(aciklama)

        # ALT SATIR
        left2, right2 = st.columns([4, 2])

        with left2:
            st.empty()

        with right2:
            badge_col, cancel_col = st.columns([2, 2])

            with badge_col:
                st.markdown(
                    f'<div class="native-badge {status}">{status_icon} {status_label}</div>',
                    unsafe_allow_html=True,
                )

            with cancel_col:
                if status == "pending" and fault.get("id"):
                    if st.button("İptal", key=f"iptal_{index}", use_container_width=True):
                        cancel_fault(fault["id"])

        st.markdown('<div class="card-gap"></div>', unsafe_allow_html=True)


def render_fault_list(faults: list[Dict]) -> None:
    if not faults:
        render_empty_state()
    else:
        for index, fault in enumerate(faults):
            render_fault_card(index, fault)


def main() -> None:
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)
    load_student_notifications_page_styles()

    student_number = get_student_no()
    faults = get_student_faults(student_number)

    pending_count, solved_count, total_count = get_status_counts(faults)

    render_back_button()
    render_stats(pending_count, solved_count, total_count)
    render_fault_list(faults)


if __name__ == "__main__":
    main()