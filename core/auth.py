# core/auth.py

import streamlit as st

from core.constants import (
    HOME_PAGE,
    ROLE_STAFF,
    ROLE_STUDENT,
    SESSION_USER,
)


def init_user_session() -> None:
    if SESSION_USER not in st.session_state:
        st.session_state[SESSION_USER] = {
            "is_logged_in": False,
            "role": None,
            "student_no": "",
            "staff_username": "",
            "name": "",
        }


def get_current_user() -> dict:
    init_user_session()
    return st.session_state[SESSION_USER]


def is_logged_in() -> bool:
    user = get_current_user()
    return bool(user.get("is_logged_in", False))


def get_user_role() -> str | None:
    user = get_current_user()
    return user.get("role")


def login_student(student_no: str, name: str = "") -> None:
    init_user_session()
    st.session_state[SESSION_USER] = {
        "is_logged_in": True,
        "role": ROLE_STUDENT,
        "student_no": student_no.strip(),
        "staff_username": "",
        "name": name.strip() if name else student_no.strip(),
    }


def login_staff(username: str, name: str = "") -> None:
    init_user_session()
    st.session_state[SESSION_USER] = {
        "is_logged_in": True,
        "role": ROLE_STAFF,
        "student_no": "",
        "staff_username": username.strip(),
        "name": name.strip() if name else username.strip(),
    }


def logout() -> None:
    st.session_state[SESSION_USER] = {
        "is_logged_in": False,
        "role": None,
        "student_no": "",
        "staff_username": "",
        "name": "",
    }

    # İsteğe bağlı geçici ekran/session temizliği
    if "admin_sub_page" in st.session_state:
        del st.session_state["admin_sub_page"]

    if "ariza_gonderildi" in st.session_state:
        del st.session_state["ariza_gonderildi"]


def require_login(required_role: str | None = None) -> bool:
    user = get_current_user()

    if not user.get("is_logged_in", False):
        return False

    if required_role and user.get("role") != required_role:
        return False

    return True


def redirect_if_not_logged_in(
    required_role: str | None = None,
    redirect_page: str = HOME_PAGE,
) -> None:
    if not require_login(required_role):
        st.warning("Bu sayfayı görüntülemek için giriş yapmalısınız.")
        st.switch_page(redirect_page)


def get_student_no() -> str:
    user = get_current_user()
    return user.get("student_no", "")


def get_staff_username() -> str:
    user = get_current_user()
    return user.get("staff_username", "")


def get_display_name(default: str = "Kullanıcı") -> str:
    user = get_current_user()
    return user.get("name") or default


def is_student() -> bool:
    return get_user_role() == ROLE_STUDENT


def is_staff() -> bool:
    return get_user_role() == ROLE_STAFF