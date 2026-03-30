from datetime import datetime
from core.database import SessionLocal
from core.models import ArizaKaydi
from core.constants import STATUS_CANCELLED, STATUS_PENDING, STATUS_SOLVED

def init_fault_state():
    """Streamlit session_state uyumluluğu için boş bırakıldı (Gerekirse kullanılabilir)."""
    pass

def add_fault(student_number: str, room_number: str, description: str):
    db = SessionLocal()
    try:
        new_record = ArizaKaydi(
            ogrenci_no=student_number.strip(),
            oda_no=room_number.strip(),
            aciklama=description.strip(),
            durum=STATUS_PENDING,
            tarih=datetime.now().strftime("%d.%m.%Y %H:%M")
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    finally:
        db.close()

def get_student_faults(student_number: str):
    db = SessionLocal()
    try:
        # Veritabanından o öğrenciye ait kayıtları çekiyoruz
        return db.query(ArizaKaydi).filter(ArizaKaydi.ogrenci_no == student_number).all()
    finally:
        db.close()

def get_status_counts(faults: list):
    """Veritabanından gelen Türkçe durum metinlerine göre sayım yapar."""
    
    # "Beklemede" olanları say
    pending_count = len([f for f in faults if f.get("durum") == "Beklemede"])
    
    # "Çözüldü" olanları say
    solved_count = len([f for f in faults if f.get("durum") == "Çözüldü"])
    
    # Toplam arıza sayısı
    total_count = len(faults)
    
    return pending_count, solved_count, total_count

def update_fault_status(fault_id: int, new_status: str) -> bool:
    db = SessionLocal()
    try:
        fault = db.query(ArizaKaydi).filter(ArizaKaydi.id == fault_id).first()
        if fault:
            fault.durum = new_status
            db.commit()
            return True
        return False
    finally:
        db.close()

def cancel_fault_by_id(fault_id: int) -> bool:
    """Öğrencinin kendi bildirimini iptal etmesi için kullanılır."""
    # Aslında bu bir durum güncellemesidir
    return update_fault_status(fault_id, STATUS_CANCELLED)

def get_status_label(status: str) -> str:
    if status == STATUS_SOLVED:
        return "Çözüldü"
    if status == STATUS_CANCELLED:
        return "İptal Edildi"
    return "Beklemede"