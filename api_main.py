import logging

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

# VERİTABANI VE GÜVENLİK İÇİN GEREKLİLER
from core.database import SessionLocal, engine
from core import models
from core.security import verify_password  # Şifre çözücü

logging.basicConfig(level=logging.INFO)

# Tabloları oluştur (Eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dormify Backend API")

@app.on_event("startup")
def ensure_tur_column_exists():
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE yemek_menusu ADD COLUMN IF NOT EXISTS tur TEXT DEFAULT 'Akşam Yemeği'"))

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veritabanı Oturumu Oluşturucu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- GEÇİCİ VERİ DEPOLARI (Duyuru için) ---
MONTHS = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]

fake_announcements_db = [
    {"baslik": "Teknik Bakım", "icerik": "İnternet çalışmaları nedeniyle kesinti yaşanabilir.", "etiket": "ACİL", "renk": "#ef4444"},
    {"baslik": "Bahar Şenliği", "icerik": "Kayıtlar lobi alanında devam etmektedir.", "etiket": "YENİ", "renk": "#3b82f6"}
]


# ---------------------------------------------------------
# 0. GİRİŞ (AUTH) İŞLEMLERİ
# ---------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/student-login", tags=["Auth"])
def student_login(req: LoginRequest, db: Session = Depends(get_db)):
    ogrenci = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == req.username).first()
    if ogrenci and verify_password(req.password, ogrenci.sifre): 
        return {"status": "success", "name": ogrenci.ad_soyad}
    raise HTTPException(status_code=401, detail="Hatalı numara veya şifre")

@app.post("/staff-login", tags=["Auth"])
def staff_login(req: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(models.Yonetici).filter(models.Yonetici.kullanici_adi == req.username).first()
    if admin and verify_password(req.password, admin.sifre):
        return {"status": "success", "name": "Yönetici"}
    raise HTTPException(status_code=401, detail="Hatalı kullanıcı adı veya şifre")


# ---------------------------------------------------------
# 1. DUYURU İŞLEMLERİ (VERİTABANI BAĞLANTILI)
# ---------------------------------------------------------
@app.get("/announcements", tags=["Duyurular"])
def list_announcements(db: Session = Depends(get_db)):
    # Duyuruları en yeniden en eskiye doğru sıralayıp gönderir
    return db.query(models.Duyuru).order_by(models.Duyuru.id.desc()).all()

@app.post("/announcements", tags=["Duyurular"])
def add_announcement(duyuru: dict, db: Session = Depends(get_db)):
    yeni_duyuru = models.Duyuru(
        baslik=duyuru.get('baslik'),
        icerik=duyuru.get('icerik'),
        etiket=duyuru.get('etiket', 'YENİ'),
        renk=duyuru.get('renk', '#3b82f6')
    )
    db.add(yeni_duyuru)
    db.commit()
    return {"status": "success", "message": "Duyuru veritabanına kaydedildi."}

@app.delete("/announcements/{duyuru_id}", tags=["Duyurular"])
def delete_announcement(duyuru_id: int, db: Session = Depends(get_db)):
    kayit = db.query(models.Duyuru).filter(models.Duyuru.id == duyuru_id).first()
    if not kayit:
        raise HTTPException(status_code=404, detail="Duyuru bulunamadı.")
    db.delete(kayit)
    db.commit()
    return {"status": "success", "message": "Duyuru başarıyla silindi."}
# ---------------------------------------------------------
# 2. YEMEKHANE İŞLEMLERİ (VERİTABANI BAĞLANTILI)
# ---------------------------------------------------------

# GÜNLÜK MENÜ - GET: Sadece bugünün tarihine denk gelen yemeği veritabanından çeker
@app.get("/meal-menu", tags=["Yemekhane"])
def get_menu(db: Session = Depends(get_db)):
    bugun = datetime.now()
    yil = bugun.year
    gun = bugun.day
    ay_adi = MONTHS[bugun.month - 1]

    gunluk_menu = db.query(models.YemekMenusu).filter(
        models.YemekMenusu.yil == yil,
        models.YemekMenusu.ay == ay_adi,
        models.YemekMenusu.gun == gun,
        models.YemekMenusu.tur == "Akşam Yemeği"  # Varsayılan olarak akşam yemeği
    ).first()

    if gunluk_menu and gunluk_menu.icerik:
        return {"menu": gunluk_menu.icerik}
    else:
        return {"menu": "Bugün için henüz yemek menüsü girilmemiştir."}

# GÜNLÜK KAHVALTI MENÜSÜ - GET
@app.get("/breakfast-menu", tags=["Yemekhane"])
def get_breakfast_menu(db: Session = Depends(get_db)):
    bugun = datetime.now()
    yil = bugun.year
    gun = bugun.day
    ay_adi = MONTHS[bugun.month - 1]

    gunluk_kahvalti = db.query(models.YemekMenusu).filter(
        models.YemekMenusu.yil == yil,
        models.YemekMenusu.ay == ay_adi,
        models.YemekMenusu.gun == gun,
        models.YemekMenusu.tur == "Kahvaltı"
    ).first()

    if gunluk_kahvalti and gunluk_kahvalti.icerik:
        return {"menu": gunluk_kahvalti.icerik}
    else:
        return {"menu": "Bugün için henüz kahvaltı menüsü girilmemiştir."}

# AYLIK MENÜ - GET: Veritabanından okuyup ön yüzün istediği formata (35 gün) çevirir
@app.get("/monthly-meal-menu", tags=["Yemekhane"])
def get_monthly_menu(yil: int = None, db: Session = Depends(get_db)):
    if yil is None:
        yil = datetime.now().year

    menu_data = {month: {str(day): "" for day in range(1, 36)} for month in MONTHS}

    kayitlar = db.query(models.YemekMenusu).filter(
        models.YemekMenusu.yil == yil,
        models.YemekMenusu.tur == "Akşam Yemeği"  # Sadece akşam yemeği kayıtları
    ).all()

    for kayit in kayitlar:
        if kayit.ay in menu_data:
            menu_data[kayit.ay][str(kayit.gun)] = kayit.icerik

    return menu_data

# AYLIK KAHVALTI MENÜSÜ - GET
@app.get("/monthly-breakfast-menu", tags=["Yemekhane"])
def get_monthly_breakfast_menu(yil: int = None, db: Session = Depends(get_db)):
    if yil is None:
        yil = datetime.now().year

    menu_data = {month: {str(day): "" for day in range(1, 36)} for month in MONTHS}

    kayitlar = db.query(models.YemekMenusu).filter(
        models.YemekMenusu.yil == yil,
        models.YemekMenusu.tur == "Kahvaltı"  # Sadece kahvaltı kayıtları
    ).all()

    for kayit in kayitlar:
        if kayit.ay in menu_data:
            menu_data[kayit.ay][str(kayit.gun)] = kayit.icerik

    return menu_data

# AYLIK MENÜ - POST: Gelen paketi veritabanına kaydeder
class MonthlyMenuPayload(BaseModel):
    yil: int
    ay: str
    tur: str  # "Kahvaltı" veya "Akşam Yemeği"
    gunler: Dict[str, str]

@app.post("/save-monthly-menu", tags=["Yemekhane"])
def save_monthly_menu(req: MonthlyMenuPayload, db: Session = Depends(get_db)):
    db.query(models.YemekMenusu).filter(
        models.YemekMenusu.yil == req.yil,
        models.YemekMenusu.ay == req.ay,
        models.YemekMenusu.tur == req.tur  # Tür'e göre filtrele
    ).delete()

    for gun_str, yemek in req.gunler.items():
        yemek_metni = str(yemek).strip()
        if yemek_metni:
            yeni_yemek = models.YemekMenusu(
                yil=req.yil,
                ay=req.ay,
                gun=int(gun_str),
                tur=req.tur,  # Tür bilgisini kaydet
                icerik=yemek_metni
            )
            db.add(yeni_yemek)

    db.commit()
    return {"status": "success", "message": "Menü başarıyla kaydedildi"}


# ---------------------------------------------------------
# 3. ÖĞRENCİ VE ARIZA İŞLEMLERİ (VERİTABANI BAĞLANTILI)
# ---------------------------------------------------------
class StudentCreate(BaseModel):
    username: str
    password: str
    full_name: str
    room_no: str

@app.post("/students/create", tags=["Öğrenciler"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == student.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu öğrenci numarası zaten kayıtlı.")

    yeni_ogrenci = models.Ogrenci(
        ogrenci_no=student.username,
        ad_soyad=student.full_name,
        oda_no=student.room_no,
        sifre=student.password,
    )
    db.add(yeni_ogrenci)
    db.commit()
    return {"status": "success", "message": "Öğrenci başarıyla kaydedildi."}

@app.get("/faults", tags=["Arıza İşlemleri"])
def list_faults(db: Session = Depends(get_db)):
    return db.query(models.ArizaKaydi).all()

@app.post("/report-fault", tags=["Arıza İşlemleri"])
def create_fault(ariza: dict, db: Session = Depends(get_db)):
    try:
        gelen_ogrenci_no = ariza.get('ogrenci_no', 'Bilinmiyor')
        
        # Görsel verisini işle (base64 string olarak)
        gorsel_data = ariza.get('gorsel')
        
        # 1. Gelen numarayla veritabanındaki öğrenciyi buluyoruz
        ogrenci = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == gelen_ogrenci_no).first()
        
        # 2. Eğer öğrenci kayıtlıysa odasını al, değilse 'Bilinmiyor' yaz
        bulunan_oda = ogrenci.oda_no if ogrenci else "Bilinmiyor"
        
        yeni_ariza = models.ArizaKaydi(
            ogrenci_no=gelen_ogrenci_no,
            baslik=ariza.get('baslik', 'Arıza Bildirimi'),
            aciklama=ariza.get('detay'),
            oda_no=bulunan_oda,  # <--- ARTIK ÖĞRENCİ TABLOSUNDAN OTOMATİK GELİYOR!
            gorsel=gorsel_data,  # Görsel verisini ekle
            durum="Beklemede"
        )
        db.add(yeni_ariza)
        db.commit()
        return {"status": "success", "message": "Arıza veritabanına kaydedildi."}
    except Exception as e:
        db.rollback()
        logging.exception("create_fault error")
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {e}")

@app.put("/update-fault/{fault_id}", tags=["Arıza İşlemleri"])
def update_fault_status(fault_id: int, yeni_durum: str, db: Session = Depends(get_db)):
    ariza = db.query(models.ArizaKaydi).filter(models.ArizaKaydi.id == fault_id).first()
    if not ariza:
        raise HTTPException(status_code=404, detail="Arıza bulunamadı.")
    ariza.durum = yeni_durum
    db.commit()
    return {"status": "success", "message": f"ID {fault_id} durumu {yeni_durum} yapıldı."}

@app.get("/student-faults/{student_no}", tags=["Arıza İşlemleri"])
def get_student_faults(student_no: str, db: Session = Depends(get_db)):
    return db.query(models.ArizaKaydi).filter(models.ArizaKaydi.ogrenci_no == student_no).all()

@app.delete("/delete-fault/{fault_id}", tags=["Arıza İşlemleri"])
def delete_fault(fault_id: int, db: Session = Depends(get_db)):
    """Veritabanından arızayı kalıcı olarak siler."""
    ariza = db.query(models.ArizaKaydi).filter(models.ArizaKaydi.id == fault_id).first()
    
    if not ariza:
        raise HTTPException(status_code=404, detail="Arıza bulunamadı.")
    
    db.delete(ariza)
    db.commit()
    return {"status": "success", "message": f"ID {fault_id} başarıyla silindi."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)