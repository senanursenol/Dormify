import streamlit as st
from typing import Dict
import base64
from binascii import Error as BinasciiError

from core.auth import get_student_no, redirect_if_not_logged_in
from core.constants import (
    ROLE_STUDENT,
    STUDENT_LOGIN_PAGE,
    STUDENT_PANEL_PAGE,
)
from core.styles import load_student_notifications_page_styles
from services.api_service import get_student_faults, get_fault_image_api
from services.fault_service import get_status_counts


def render_back_button() -> None:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Ana Panele Dön"):
        st.switch_page(STUDENT_PANEL_PAGE)
    st.markdown("</div>", unsafe_allow_html=True)


def render_stats(pending_count: int, solved_count: int, total_count: int) -> None:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">⏳</div><div class="stat-number">{pending_count}</div><div class="stat-label">Beklemede</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">✅</div><div class="stat-number">{solved_count}</div><div class="stat-label">Çözüldü</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-icon">📋</div><div class="stat-number">{total_count}</div><div class="stat-label">Toplam</div></div>', unsafe_allow_html=True)


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-state" style="text-align: center; padding: 3rem; background-color: #f8fafc; border-radius: 12px; border: 1px dashed #cbd5e1; margin-top: 20px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📭</div>
            <h3 style="color: #334155; margin:0;">Kayıt Bulunmuyor</h3>
            <p style="color: #64748b; margin-top: 5px;">Henüz bir arıza bildirimi oluşturmadınız.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_status_info(fault: Dict) -> tuple[str, str, str]:
    db_durum = fault.get("durum", "Beklemede")
    if db_durum == "Çözüldü": return "solved", "Çözüldü", "✅"
    elif db_durum == "İptal Edildi": return "cancelled", "İptal", "❌"
    else: return "pending", "Beklemede", "⏳"


def decode_base64_image(image_value):
    if not isinstance(image_value, str): return image_value
    if image_value.startswith("data:image"):
        try:
            _, _, data = image_value.partition(",")
            return base64.b64decode(data)
        except (BinasciiError, ValueError): return image_value
    try:
        return base64.b64decode(image_value)
    except (BinasciiError, ValueError): return image_value


def render_fault_card(index: int, fault: Dict) -> None:
    status, status_label, status_icon = get_status_info(fault)
    fault_id = fault.get("id")
    tarih = fault.get("tarih", "-")
    aciklama = fault.get("aciklama") or fault.get("detay") or "Açıklama belirtilmedi."
    baslik = fault.get("baslik", "Arıza Bildirimi")

    with st.container(border=True):
        # 1. SATIR: Başlık ve Rozet (Yan yana çok şık duracak)
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"**📌 {baslik}**")
            st.caption(f"📅 Tarih: {tarih}")
        with c2:
            st.markdown(f'<div class="native-badge {status}" style="float: right; margin-top: 5px;">{status_icon} {status_label}</div>', unsafe_allow_html=True)
        
        # Hafif bir çizgi ile metni ayıralım
        st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)
        
        # 2. SATIR: Açıklama (Zarif bir gri tonla)
        st.markdown(f"<div style='color: #475569; font-size: 0.95rem; margin-bottom: 12px; line-height: 1.5;'>{aciklama}</div>", unsafe_allow_html=True)
        
        # 3. SATIR: Görsel Butonu ve Gösterim Alanı
        gorsel_tutucu = st.empty()
        
        # Butonu küçük ve kibar yapıyoruz
        if st.button("🖼️ Görseli Yükle", key=f"img_btn_{fault_id}", help="Tıklayarak fotoğrafı görebilirsiniz"):
            with st.spinner("Yükleniyor..."):
                gorsel_base64 = get_fault_image_api(fault_id)
                if gorsel_base64:
                    g = decode_base64_image(gorsel_base64)
                    if g: 
                        gorsel_tutucu.image(g, width="stretch")
                else:
                    gorsel_tutucu.markdown("*Bu arızaya ait bir görsel eklenmemiş.*")


def main() -> None:
    redirect_if_not_logged_in(ROLE_STUDENT, STUDENT_LOGIN_PAGE)
    load_student_notifications_page_styles()

    student_number = get_student_no()
    faults = get_student_faults(student_number)
    pending_count, solved_count, total_count = get_status_counts(faults)

    render_back_button()
    render_stats(pending_count, solved_count, total_count)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Gönderdiğiniz Arıza Kayıtları")
    
    if not faults:
        render_empty_state()
    else:
        for index, fault in enumerate(faults):
            render_fault_card(index, fault)


if __name__ == "__main__":
    main()