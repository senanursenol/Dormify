from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Uygulama Başlatma
app = FastAPI(
    title="Dormify Backend API",
    description="Yurt Yönetim Sistemi için Arka Plan Servisi",
    version="1.1.0"
)

# ---------------------------------------------------------
# 1. GÜVENLİK AYARLARI (CORS)
# ---------------------------------------------------------
# Streamlit (Frontend) ile iletişimi sağlar.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. VERİ MODELLERİ (SCHEMAS)
# ---------------------------------------------------------
class ArizaKaydi(BaseModel):
    baslik: str
    detay: str
    oda_no: str
    durum: Optional[str] = "Beklemede"

class Duyuru(BaseModel):
    baslik: str
    icerik: str
    etiket: Optional[str] = "YENİ"
    renk: Optional[str] = "#3b82f6"

# ---------------------------------------------------------
# 3. GEÇİCİ VERİ DEPOSU (MOCK DATABASE)
# ---------------------------------------------------------
# NOT: Arkadaşın buradaki listeleri SQL Veritabanına bağlayacak.
fake_faults_db = [] 

fake_announcements_db = [
    {
        "baslik": "Teknik Bakım Duyurusu",
        "icerik": "İnternet çalışmaları nedeniyle kesinti yaşanabilir.",
        "etiket": "ACİL",
        "renk": "#ef4444",
    },
    {
        "baslik": "Bahar Şenliği",
        "icerik": "Kayıtlar lobi alanında devam etmektedir.",
        "etiket": "YENİ",
        "renk": "#3b82f6",
    }
]

fake_meal_db = {"menu": "Yayla Çorbası, Tavuk Sote, Pilav, Meyve"}

# ---------------------------------------------------------
# 4. DUYURU İŞLEMLERİ (ENDPOINTS)
# ---------------------------------------------------------

@app.get("/announcements", response_model=List[Duyuru], tags=["Duyurular"])
def get_announcements():
    """Sistemdeki tüm güncel duyuruları listeler."""
    return fake_announcements_db

@app.post("/announcements", tags=["Duyurular"])
def add_announcement(duyuru: Duyuru):
    """Yeni bir duyuru yayınlar ve listenin başına ekler."""
    try:
        fake_announcements_db.insert(0, duyuru.dict())
        return {"status": "success", "message": "Duyuru başarıyla yayınlandı."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 5. YEMEKHANE İŞLEMLERİ (ENDPOINTS)
# ---------------------------------------------------------

@app.get("/meal-menu", tags=["Yemekhane"])
def get_menu():
    """Günün mevcut yemek menüsünü getirir."""
    return fake_meal_db

@app.put("/meal-menu", tags=["Yemekhane"])
def update_meal(menu_text: str):
    """Mevcut yemek menüsünü günceller."""
    try:
        fake_meal_db["menu"] = menu_text
        return {"status": "success", "message": "Menü güncellendi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 6. ARIZA İŞLEMLERİ (ENDPOINTS)
# ---------------------------------------------------------

@app.get("/faults", response_model=List[ArizaKaydi], tags=["Arıza İşlemleri"])
def list_faults():
    """Personel için tüm arıza kayıtlarını listeler."""
    return fake_faults_db

@app.post("/report-fault", tags=["Arıza İşlemleri"])
def create_fault(ariza: ArizaKaydi):
    """Öğrenci arıza bildirimini kaydeder."""
    try:
        fake_faults_db.append(ariza.dict())
        return {"status": "success", "message": "Arıza kaydedildi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update-fault/{fault_id}", tags=["Arıza İşlemleri"])
def update_fault_status(fault_id: int, yeni_durum: str):
    """Belirli bir arızanın durumunu günceller."""
    try:
        if 0 <= fault_id < len(fake_faults_db):
            fake_faults_db[fault_id]["durum"] = yeni_durum
            return {"status": "success", "message": f"Durum {yeni_durum} yapıldı."}
        raise HTTPException(status_code=404, detail="Arıza bulunamadı.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Genel"])
def read_root():
    return {"status": "Success", "message": "Dormify API is Online"}