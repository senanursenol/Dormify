from datetime import datetime
from uuid import uuid4

import streamlit as st

from core.constants import (
    SESSION_FAULTS,
    STATUS_CANCELLED,
    STATUS_PENDING,
    STATUS_SOLVED,
)


def init_fault_state() -> None:
    if SESSION_FAULTS not in st.session_state:
        st.session_state[SESSION_FAULTS] = []


def get_all_faults() -> list[dict]:
    init_fault_state()
    return st.session_state[SESSION_FAULTS]


def add_fault(student_number: str, room_number: str, description: str) -> dict:
    init_fault_state()

    new_record = {
        "id": str(uuid4()),
        "ogrenci_no": student_number.strip(),
        "oda_no": room_number.strip(),
        "aciklama": description.strip(),
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "durum": STATUS_PENDING,
    }

    st.session_state[SESSION_FAULTS].insert(0, new_record)
    return new_record


def get_student_faults(student_number: str) -> list[dict]:
    init_fault_state()
    return [
        fault
        for fault in st.session_state[SESSION_FAULTS]
        if fault.get("ogrenci_no") == student_number
    ]


def get_status_counts(faults: list[dict]) -> tuple[int, int, int]:
    pending_count = len([f for f in faults if f.get("durum") == STATUS_PENDING])
    solved_count = len([f for f in faults if f.get("durum") == STATUS_SOLVED])
    total_count = len(faults)
    return pending_count, solved_count, total_count


def cancel_fault_by_id(fault_id: str) -> bool:
    init_fault_state()

    updated_faults = []
    found = False

    for fault in st.session_state[SESSION_FAULTS]:
        if fault.get("id") == fault_id:
            updated_faults.append({**fault, "durum": STATUS_CANCELLED})
            found = True
        else:
            updated_faults.append(fault)

    st.session_state[SESSION_FAULTS] = updated_faults
    return found


def update_fault_status(fault_id: str, new_status: str) -> bool:
    init_fault_state()

    if new_status not in {STATUS_PENDING, STATUS_SOLVED, STATUS_CANCELLED}:
        return False

    updated_faults = []
    found = False

    for fault in st.session_state[SESSION_FAULTS]:
        if fault.get("id") == fault_id:
            updated_faults.append({**fault, "durum": new_status})
            found = True
        else:
            updated_faults.append(fault)

    st.session_state[SESSION_FAULTS] = updated_faults
    return found


def get_status_label(status: str) -> str:
    if status == STATUS_SOLVED:
        return "Çözüldü"
    if status == STATUS_CANCELLED:
        return "İptal Edildi"
    return "Beklemede"