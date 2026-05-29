🚀 Dormify | Yeni Nesil Yurt Yönetim Sistemi
Dormify, öğrenci yurdu operasyonlarını dijitalleştirerek kağıt israfını önleyen, yönetim ile öğrenciler arasındaki iletişimi hızlandıran modern bir Yurt Yönetim Platformu'dur.

📋 Proje Özeti
Dormify, özel yurtlarda karşılaşılan temel sorunları çözmek amacıyla geliştirilmiştir:

Operasyonel Verimlilik: Arıza bildirimlerinin tek bir yerden takibi ve yönetimi.

Dijital İletişim: Duyuru ve etkinliklerin görsel destekli yönetimi.

Şeffaf Hizmet: Günlük ve aylık yemek menüsü planlaması.

Güvenli Erişim: Öğrenci ve Personel için ayrı giriş yetkilendirmeleri.

🛠️ Teknik Altyapı
Proje, katmanlı mimari prensiplerine göre modüler olarak geliştirilmiştir:

Backend: FastAPI (Yüksek performanslı API yapısı)

Frontend: Streamlit (Hızlı, interaktif kullanıcı arayüzü)

Veritabanı: SQLAlchemy ORM (PostgreSQL/SQLite destekli)

Güvenlik: bcrypt (Şifre hashleme), python-dotenv (Çevresel değişken yönetimi)

Görüntü İşleme: Pillow (Otomatik görsel sıkıştırma ve optimizasyon)

✨ Temel Özellikler
Arıza Yönetim Sistemi: Öğrenciler arıza kaydı oluşturabilir, personel bu kayıtları inceleyip durumlarını (Beklemede/İşlemde/Tamamlandı) güncelleyebilir.

Akıllı Duyuru Paneli: Personel tarafından girilen duyurular anlık olarak ön yüzde görsel destekli slider'da gösterilir.

Yemekhane Yönetimi: Kahvaltı ve akşam yemeği menüleri günlük/aylık olarak yönetilebilir; takvim görünümü ile şık bir deneyim sunulur.

Güvenlik: Öğrenci ve personelin yetkisiz erişimini engelleyen rol tabanlı giriş sistemi.

🚀 Kurulum
1. Hazırlık
Proje dizininde bir sanal ortam oluşturup aktif edin:
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate

2. Bağımlılıkları Yükleyin
pip install -r requirements.txt

3. Sistemi Başlatın
Sistemin çalışması için iki servisin de aynı anda aktif olması gerekir:

Backend API:
uvicorn api_main:app --reload

Frontend (UI):
streamlit run app.py

👤 İletişim & Geliştirici
Bu proje, yurt operasyonlarını dijitalleştirmek isteyen kurumlar için geliştirilmiş bir prototiptir.

GitHub: senanursenol/Dormify

Not: Bu proje, Clean Code prensipleri gözetilerek; veritabanı bağlantılarının güvenliği, modüler kod yapısı ve kullanıcı odaklı tasarım ilkeleriyle geliştirilmiştir.

