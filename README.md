# Dormify | Yeni Nesil Yurt Yönetim Sistemi

Dormify, öğrenci yurtlarında günlük operasyonları dijitalleştirmek amacıyla geliştirilmiş modern bir yurt yönetim sistemidir. Proje; öğrenci girişi, arıza bildirimi, bildirim takibi, personel yönetimi ve yurt içi süreçlerin daha düzenli yürütülmesini hedefler.

## Proje Özeti

Dormify ile öğrenciler yurtta karşılaştıkları arızaları kolayca bildirebilir, oluşturdukları kayıtların durumunu takip edebilir ve yurt işlemlerini dijital ortamdan yönetebilir. Sistem, öğrenci ve personel rolleri için ayrı erişim yapısı sunar.

## Temel Özellikler

- Öğrenci giriş sistemi
- Rol bazlı oturum yönetimi
- Öğrenci paneli
- Arıza bildirimi oluşturma
- Arıza açıklaması ve oda numarası doğrulama
- Gönderilen arıza bildirimlerini listeleme
- Bildirim durumlarını takip etme
  - Beklemede
  - Çözüldü
  - İptal Edildi
- Bildirim iptal etme
- Modern ve responsive Streamlit arayüzü
- Ortak CSS/stil yönetimi
- Logo ve sayfa bileşenleri için modüler yapı

## Kullanılan Teknolojiler

- Python
- Streamlit
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- bcrypt
- python-dotenv
- Pillow

## Proje Yapısı

```text
Dormify/
│
├── app.py
├── api_main.py
├── admin_olustur.py
├── ogrenci_olustur.py
│
├── assets/
│   └── logo.png
│
├── core/
│   ├── auth.py
│   ├── constants.py
│   ├── styles.py
│   └── ui.py
│
├── pages/
│   ├── ogrenci_giris.py
│   ├── ogrenci_panel.py
│   ├── ogrenci_ariza.py
│   ├── ogrenci_bildirimler.py
│   ├── personel_giris.py
│   └── personel_panel.py
│
└── services/
    └── fault_service.py
```

## Kurulum

### 1. Projeyi klonlayın

```bash
git clone https://github.com/senanursenol/Dormify.git
cd Dormify
```

### 2. Sanal ortam oluşturun

```bash
python -m venv venv
```

Windows için:

```bash
venv\Scripts\activate
```

macOS / Linux için:

```bash
source venv/bin/activate
```

### 3. Gerekli paketleri yükleyin

```bash
pip install -r requirements.txt
```

Eğer `requirements.txt` yoksa temel kurulum için:

```bash
pip install streamlit fastapi uvicorn sqlalchemy bcrypt python-dotenv pillow
```

## Çalıştırma

Streamlit arayüzünü başlatmak için:

```bash
streamlit run app.py
```

FastAPI tarafını çalıştırmak için:

```bash
uvicorn api_main:app --reload
```

## Öğrenci Kullanım Akışı

1. Öğrenci giriş sayfasından öğrenci numarası ve şifre ile giriş yapar.
2. Öğrenci paneline yönlendirilir.
3. “Yeni Arıza Bildir” seçeneği ile arıza kaydı oluşturur.
4. Oda numarası ve arıza açıklaması girilir.
5. Bildirim başarıyla kaydedilir.
6. “Bildirimleri Gör” sayfasından arıza kayıtlarının durumu takip edilir.
7. Beklemede olan bildirimler iptal edilebilir.

## Oturum ve Rol Yönetimi

Sistemde öğrenci ve personel rolleri ayrılmıştır. Kullanıcı giriş yaptığında oturum bilgileri Streamlit session state üzerinde tutulur. Yetkisiz kullanıcılar ilgili sayfalara erişmeye çalıştığında giriş sayfasına yönlendirilir.

## Arıza Durumları

Arıza kayıtları üç temel durumda takip edilir:

| Durum | Açıklama |
|---|---|
| Beklemede | Arıza bildirimi oluşturulmuş, henüz çözülmemiştir. |
| Çözüldü | Arıza personel tarafından çözülmüştür. |
| İptal Edildi | Öğrenci veya sistem tarafından bildirim iptal edilmiştir. |

## Ekranlar

- Ana sayfa
- Öğrenci giriş sayfası
- Öğrenci paneli
- Arıza bildirimi sayfası
- Bildirimlerim sayfası
- Personel giriş sayfası
- Personel paneli

## Geliştirici Notları

Proje modüler bir yapıda geliştirilmiştir:

- `core/auth.py`: Oturum ve rol yönetimi
- `core/constants.py`: Sayfa yolları, roller ve sabit değerler
- `core/styles.py`: Ortak CSS ve sayfa stilleri
- `core/ui.py`: Ortak arayüz bileşenleri
- `services/fault_service.py`: Arıza kayıt işlemleri
- `pages/`: Streamlit sayfaları

## Hedef

Dormify, yurt yönetim süreçlerinde kağıt kullanımını azaltmayı, öğrenci-personel iletişimini hızlandırmayı ve arıza/bildirim takibini daha düzenli hale getirmeyi amaçlar.

## Geliştirici

**Senanur Şenol**  
GitHub: [senanursenol](https://github.com/senanursenol)
