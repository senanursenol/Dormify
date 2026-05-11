import logging
import io
import base64

from sqlalchemy.orm import defer
from PIL import Image
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import or_

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
    
    # --- GÖRSEL SIKIŞTIRMA MANTIĞI (Arızalardaki gibi) ---
    gorsel_verisi = duyuru.get('gorsel')
    if gorsel_verisi and len(gorsel_verisi) > 100:
        try:
            import io, base64
            from PIL import Image
            
            # Başında "data:image..." varsa ayıklıyoruz, yoksa direkt alıyoruz
            header, encoded = gorsel_verisi.split(",", 1) if "," in gorsel_verisi else ("", gorsel_verisi)
            image_data = base64.b64decode(encoded)
            image = Image.open(io.BytesIO(image_data))
            
            # Şeffaf PNG ise RGB'ye çevirip arka planı düzeltiyoruz
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Duyuru afişi olduğu için boyutu 1000x1000 yapalım (biraz daha net olsun)
            image.thumbnail((1000, 1000)) 
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='JPEG', quality=65, optimize=True)
            
            # Veritabanına temiz ve küçücük bir metin olarak kaydediyoruz
            gorsel_verisi = f"data:image/jpeg;base64,{base64.b64encode(byte_arr.getvalue()).decode('utf-8')}"
            print("✅ Duyuru afişi başarıyla sıkıştırıldı!")
        except Exception as e:
            print(f"⚠️ Duyuru görseli sıkıştırma hatası: {e}")
            gorsel_verisi = None
    # -------------------------------------------------------

    yeni_duyuru = models.Duyuru(
        baslik=duyuru.get('baslik'),
        icerik=duyuru.get('icerik'),
        gorsel=gorsel_verisi, # Artık sıkıştırılmış küçük görsel gidiyor
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
def get_all_faults(db: Session = Depends(get_db)):
    try:
        # SİHİRLİ SATIR: Görsel sütununu çekmeyi erteliyoruz (.options(defer(...)))
        arizalar = db.query(models.ArizaKaydi).options(
            defer(models.ArizaKaydi.gorsel)
        ).order_by(models.ArizaKaydi.id.desc()).all()
        
        # Sonuçları personele göndermeden önce "Numaraları İsimlerle" değiştiriyoruz
        sonuclar = []
        for a in arizalar:
            ogrenci = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == a.ogrenci_no).first()
            gosterilecek_isim = ogrenci.ad_soyad if ogrenci else a.ogrenci_no
            
            sonuclar.append({
                "id": a.id,
                "ogrenci_no": gosterilecek_isim, # <--- Personel paneline numarayı değil ismi gönderiyoruz!
                "oda_no": a.oda_no,
                "baslik": a.baslik,
                "aciklama": a.aciklama,
                "durum": a.durum,
                "tarih": a.tarih
            })
            
        return sonuclar
    except Exception as e:
        print(f"🔥 GET TÜM ARIZALAR HATASI: {e}")
        return []

@app.post("/report-fault", tags=["Arıza İşlemleri"])
def create_fault(ariza: dict, db: Session = Depends(get_db)):
    try:
        gelen_no = str(ariza.get('ogrenci_no', '')).strip()
        print(f"🔍 Arıza bildirimi geldi. Aranan Öğrenci No: '{gelen_no}'")

        ogrenci = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == gelen_no).first()
        
        if ogrenci:
            print(f"✅ Öğrenci Bulundu: {ogrenci.ad_soyad}, Oda: {ogrenci.oda_no}")
            bulunan_oda = ogrenci.oda_no
        else:
            print(f"❌ HATA: Öğrenci bulunamadı!")
            bulunan_oda = "Bilinmiyor"

        # --- GÜNCELLENEN GÖRSEL SIKIŞTIRMA KISMI ---
        gorsel_verisi = ariza.get('gorsel')
        if gorsel_verisi and len(gorsel_verisi) > 100:
            try:
                import io, base64
                from PIL import Image
                header, encoded = gorsel_verisi.split(",", 1) if "," in gorsel_verisi else ("", gorsel_verisi)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
                
                # SİHİRLİ SATIR: Eğer görsel PNG/RGBA (şeffaf) ise, onu JPEG uyumlu RGB'ye çevir!
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                    
                image.thumbnail((800, 800))
                byte_arr = io.BytesIO()
                image.save(byte_arr, format='JPEG', quality=60, optimize=True)
                gorsel_verisi = f"data:image/jpeg;base64,{base64.b64encode(byte_arr.getvalue()).decode('utf-8')}"
                print("✅ Görsel başarıyla sıkıştırıldı!")
            except Exception as img_err:
                print(f"⚠️ Görsel sıkıştırma hatası: {img_err}")
                # Görsel sıkıştırılamazsa veritabanını çökertmemek için görseli boş gönderiyoruz
                gorsel_verisi = None 
        # ------------------------------------------

        yeni_ariza = models.ArizaKaydi(
            ogrenci_no=gelen_no,  # <--- DÜZELTME: Veritabanına isim değil, numara kaydediyoruz!
            baslik=ariza.get('baslik', 'Arıza Bildirimi'),
            aciklama=ariza.get('detay'),
            oda_no=bulunan_oda,
            gorsel=gorsel_verisi,
            durum="Beklemede"
        )
        db.add(yeni_ariza)
        db.commit()
        db.refresh(yeni_ariza)
        print("✅ Arıza veritabanına başarıyla kaydedildi!")
        return {"status": "success"}
        
    except Exception as e:
        db.rollback()
        print(f"🔥 Kritik Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/update-fault/{fault_id}", tags=["Arıza İşlemleri"])
def update_fault_status(fault_id: int, yeni_durum: str, db: Session = Depends(get_db)):
    ariza = db.query(models.ArizaKaydi).filter(models.ArizaKaydi.id == fault_id).first()
    if not ariza:
        raise HTTPException(status_code=404, detail="Arıza bulunamadı.")
    ariza.durum = yeni_durum
    db.commit()
    return {"status": "success", "message": f"ID {fault_id} durumu {yeni_durum} yapıldı."}

from sqlalchemy import or_

@app.get("/student-faults/{student_number}")
def get_student_faults(student_number: str, db: Session = Depends(get_db)):
    from sqlalchemy.orm import defer
    
    try:
        # 1. Önce bu numaranın kime ait olduğunu (ismini) bulalım
        ogrenci = db.query(models.Ogrenci).filter(models.Ogrenci.ogrenci_no == student_number).first()
        aranacak_isim = ogrenci.ad_soyad if ogrenci else "Bilinmiyor"

        # 2. Veritabanında HEM numarayı HEM de ismi arayalım! 
        # (Böylece eski hatalı kayıtlar da yeni doğru kayıtlar da listelenir)
        arizalar = db.query(models.ArizaKaydi).filter(
            or_(
                models.ArizaKaydi.ogrenci_no == student_number,
                models.ArizaKaydi.ogrenci_no == aranacak_isim
            )
        ).options(defer(models.ArizaKaydi.gorsel)).order_by(models.ArizaKaydi.id.desc()).all()
        
        print(f"✅ Öğrenci paneli için {len(arizalar)} adet arıza başarıyla çekildi!")
        return arizalar
        
    except Exception as e:
        print(f"🔥 GET ÖĞRENCİ ARIZALARI HATASI: {e}")
        return []

@app.get("/fault-image/{fault_id}", tags=["Arıza İşlemleri"])
def get_fault_image(fault_id: int, db: Session = Depends(get_db)):
    # Sadece o ID'ye ait arızayı bul
    ariza = db.query(models.ArizaKaydi).filter(models.ArizaKaydi.id == fault_id).first()
    if ariza and ariza.gorsel:
        return {"gorsel": ariza.gorsel}
    return {"gorsel": None}

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