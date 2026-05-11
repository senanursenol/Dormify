from sqlalchemy import Column, Integer, String, Text
from datetime import datetime
from .database import Base, engine

class Yonetici(Base):
    __tablename__ = "yoneticiler"
    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String(50), unique=True)
    sifre = Column(String(100)) 

class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    
    id = Column(Integer, primary_key=True, index=True)
    ogrenci_no = Column(String(20), unique=True, nullable=False)
    ad_soyad = Column(String(100))
    oda_no = Column(String(10))
    sifre = Column(String(100))

class ArizaKaydi(Base):
    __tablename__ = "arizalar"
    
    id = Column(Integer, primary_key=True, index=True)
    ogrenci_no = Column(String(20), nullable=False)
    oda_no = Column(String(10))
    baslik = Column(String(100))
    aciklama = Column(Text)
    gorsel = Column(Text, nullable=True)  # Görsel eklendi
    tarih = Column(String(50), default=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))
    durum = Column(String(20), default="Beklemede")

class Duyuru(Base):
    __tablename__ = "duyurular"
    
    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(100))
    icerik = Column(Text)
    gorsel = Column(Text, nullable=True) # EKSİK OLAN GÖRSEL SÜTUNU EKLENDİ!
    etiket = Column(String(20), default="YENİ")
    renk = Column(String(20), default="#3b82f6")
    tarih = Column(String(50), default=lambda: datetime.now().strftime("%d.%m.%Y %H:%M"))

class YemekMenusu(Base):
    __tablename__ = "yemek_menusu"
    
    id = Column(Integer, primary_key=True, index=True)
    yil = Column(Integer, index=True)        
    ay = Column(String(20), index=True)      
    gun = Column(Integer)                    
    tur = Column(String(20), default="Akşam Yemeği")  
    icerik = Column(Text)                    

# Modelleri veritabanına yazar
Base.metadata.create_all(bind=engine)