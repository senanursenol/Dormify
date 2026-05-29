# 🚀 Dormify | Yeni Nesil Yurt Yönetim Sistemi

**Dormify**, öğrenci yurdu operasyonlarını dijitalleştirerek kağıt israfını önleyen, yönetim ile öğrenciler arasındaki iletişimi hızlandıran modern bir **Yurt Yönetim Platformu**'dur.

---

## 📋 Proje Özeti
Dormify, özel yurtlarda karşılaşılan temel sorunları çözmek amacıyla geliştirilmiştir:
- **Operasyonel Verimlilik:** Arıza bildirimlerinin tek bir yerden takibi ve yönetimi.
- **Dijital İletişim:** Duyuru ve etkinliklerin görsel destekli yönetimi.
- **Şeffaf Hizmet:** Günlük ve aylık yemek menüsü planlaması.
- **Güvenli Erişim:** Öğrenci ve Personel için ayrı giriş yetkilendirmeleri.

---

## 🛠️ Teknik Altyapı
Proje, katmanlı mimari prensiplerine göre modüler olarak geliştirilmiştir:

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Yüksek performanslı API yapısı)
* **Frontend:** [Streamlit](https://streamlit.io/) (Hızlı, interaktif kullanıcı arayüzü)
* **Veritabanı:** [SQLAlchemy](https://www.sqlalchemy.org/) ORM (PostgreSQL/SQLite destekli)
* **Güvenlik:** `bcrypt` (Şifre hashleme), `python-dotenv` (Çevresel değişken yönetimi)
* **Görüntü İşleme:** `Pillow` (Otomatik görsel sıkıştırma ve optimizasyon)

---

## ✨ Temel Özellikler
1. **Arıza Yönetim Sistemi:** Öğrenciler arıza kaydı oluşturabilir, personel bu kayıtları inceleyip durumlarını güncelleyebilir.
2. **Akıllı Duyuru Paneli:** Personel tarafından girilen duyurular anlık olarak görsel destekli slider'da gösterilir.
3. **Yemekhane Yönetimi:** Kahvaltı ve akşam yemeği menüleri günlük/aylık olarak yönetilebilir; takvim görünümü ile şık bir deneyim sunulur.
4. **Güvenlik:** Öğrenci ve personelin yetkisiz erişimini engelleyen rol tabanlı giriş sistemi.

---

## 🚀 Kurulum
### 1. Hazırlık
Proje dizininde bir sanal ortam oluşturup aktif edin:
```bash
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

---

## 2.Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt

---

## 3. Sistemi Başlatın
Sistemin çalışması için iki servisin de aynı anda aktif olması gerekir:

Backend API:
```bash
uvicorn api_main:app --reload

Frontend (UI):
```bash
streamlit run app.py

---

👤 İletişim & Geliştirici
Bu proje, yurt operasyonlarını dijitalleştirmek isteyen kurumlar için geliştirilmiş bir prototiptir.

GitHub: senanursenol/Dormify

Not: Bu proje, Clean Code prensipleri gözetilerek; veritabanı bağlantılarının güvenliği, modüler kod yapısı ve kullanıcı odaklı tasarım ilkeleriyle geliştirilmiştir.
