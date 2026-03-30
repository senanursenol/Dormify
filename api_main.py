from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

# VERİTABANI BAĞLANTISI İÇİN GEREKLİLER
from core.database import SessionLocal, engine
from core import models

# Tabloları oluştur (Eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dormify Backend API")

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

# --- GEÇİCİ VERİ DEPOLARI (Şimdilik Duyuru ve Yemek için) ---
fake_announcements_db = [
    {"baslik": "Teknik Bakım", "icerik": "İnternet çalışmaları nedeniyle kesinti yaşanabilir.", "etiket": "ACİL", "renk": "#ef4444"},
    {"baslik": "Bahar Şenliği", "icerik": "Kayıtlar lobi alanında devam etmektedir.", "etiket": "YENİ", "renk": "#3b82f6"}
]
fake_meal_db = {"menu": "Yayla Çorbası, Tavuk Sote, Pilav, Meyve"}

# ---------------------------------------------------------
# 1. DUYURU İŞLEMLERİ
# ---------------------------------------------------------
@app.get("/announcements", tags=["Duyurular"])
def list_announcements():
    return fake_announcements_db

@app.post("/announcements", tags=["Duyurular"])
def add_announcement(duyuru: dict):
    fake_announcements_db.insert(0, duyuru)
    return {"status": "success", "message": "Duyuru yayınlandı."}

# ---------------------------------------------------------
# 2. YEMEKHANE İŞLEMLERİ
# ---------------------------------------------------------
@app.get("/meal-menu", tags=["Yemekhane"])
def get_menu():
    return fake_meal_db

@app.put("/meal-menu", tags=["Yemekhane"])
def update_meal(menu_text: str):
    fake_meal_db["menu"] = menu_text
    return {"status": "success", "message": "Menü güncellendi."}

# ---------------------------------------------------------
# 3. ARIZA İŞLEMLERİ (VERİTABANI BAĞLANTILI)
# ---------------------------------------------------------
@app.get("/faults", tags=["Arıza İşlemleri"])
def list_faults(db: Session = Depends(get_db)):
    return db.query(models.ArizaKaydi).all()

@app.post("/report-fault", tags=["Arıza İşlemleri"])
def create_fault(ariza: dict, db: Session = Depends(get_db)):
    try:
        yeni_ariza = models.ArizaKaydi(
            ogrenci_no=ariza.get('ogrenci_no', 'Bilinmiyor'), # Öğrenci No ekledik!
            baslik=ariza['baslik'],
            aciklama=ariza['detay'],
            oda_no=ariza['oda_no'],
            durum="Beklemede"
        )
        db.add(yeni_ariza)
        db.commit()
        return {"status": "success", "message": "Arıza veritabanına kaydedildi."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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

# api_main.py içindeki Arıza İşlemleri bölümünün sonuna ekle:

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