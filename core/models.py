from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
# database.py dosyasından Base ve engine'i içeri alıyoruz
from .database import Base, engine

class Yonetici(Base):
    __tablename__ = "yoneticiler"
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String(50), unique=True)
    sifre = Column(String(100)) # Gerçek projelerde bu şifrelenir (hash)


class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    
    id = Column(Integer, primary_key=True, index=True)
    ogrenci_no = Column(String(20), unique=True, nullable=False)
    ad_soyad = Column(String(100))
    oda_no = Column(String(10))
    sifre = Column(String(100)) # Başlangıç şifresi

class ArizaKaydi(Base):
    __tablename__ = "arizalar"
    
    id = Column(Integer, primary_key=True, index=True)
    ogrenci_no = Column(String(20), nullable=False)
    oda_no = Column(String(10))
    baslik = Column(String(100))
    aciklama = Column(Text)
    tarih = Column(String(50), default=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))
    durum = Column(String(20), default="Beklemede")
Base.metadata.create_all(bind=engine)