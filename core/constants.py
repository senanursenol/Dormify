# core/constants.py

# Sayfa yolları
HOME_PAGE = "app.py"

# Öğrenci sayfaları
STUDENT_LOGIN_PAGE = "pages/ogrenci_giris.py"
STUDENT_PANEL_PAGE = "pages/ogrenci_panel.py"
STUDENT_FAULT_PAGE = "pages/ogrenci_ariza.py"
STUDENT_NOTIFICATIONS_PAGE = "pages/ogrenci_bildirimler.py"

# Personel sayfaları (şimdilik placeholder olabilir)
STAFF_LOGIN_PAGE = "pages/personel_giris.py"
STAFF_PANEL_PAGE = "pages/personel_panel.py"

# Roller
ROLE_STUDENT = "student"
ROLE_STAFF = "staff"

# Arıza durumları
STATUS_PENDING = "pending"
STATUS_SOLVED = "solved"
STATUS_CANCELLED = "cancelled"

# Session key'leri
SESSION_USER = "user"
SESSION_FAULTS = "ariza_listesi"
SESSION_FAULT_SENT = "ariza_gonderildi"