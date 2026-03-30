from core.database import SessionLocal
from core.models import Yonetici

def admin_ekle():
    db = SessionLocal()
    try:
        # Önce bu kullanıcı zaten var mı kontrol edelim
        var_mi = db.query(Yonetici).filter(Yonetici.kullanici_adi == "admin").first()
        
        if not var_mi:
            yeni_admin = Yonetici(
                kullanici_adi="admin", 
                sifre="123456" # Burayı istediğin güvenli bir şifreyle değiştir!
            )
            db.add(yeni_admin)
            db.commit()
            print("✅ Yönetici başarıyla oluşturuldu!")
        else:
            print("ℹ️ Bu kullanıcı adı zaten mevcut.")
            
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    admin_ekle()