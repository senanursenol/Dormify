from core.database import SessionLocal
from core.models import Ogrenci

def ogrenci_ekle():
    db = SessionLocal()
    try:
        # Örnek bir öğrenci verisi
        yeni_no = "220309017"
        
        # Bu numarayla kayıt var mı kontrol et
        var_mi = db.query(Ogrenci).filter(Ogrenci.ogrenci_no == yeni_no).first()
        
        if not var_mi:
            yeni_ogrenci = Ogrenci(
                ogrenci_no=yeni_no,
                ad_soyad="Elif Kurtarmış",
                oda_no="204",
                sifre="elif123"
            )
            db.add(yeni_ogrenci)
            db.commit()
            print(f"✅ Öğrenci {yeni_no} başarıyla oluşturuldu!")
        else:
            print("ℹ️ Bu öğrenci numarası zaten sistemde kayıtlı.")
            
    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    ogrenci_ekle()