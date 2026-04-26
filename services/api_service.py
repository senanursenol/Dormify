import requests
import streamlit as st

# FastAPI sunucusunun çalıştığı adres ve port
BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------
# 1. DUYURU İŞLEMLERİ (GET & POST)
# ---------------------------------------------------------

def get_announcements():
    """FastAPI'den tüm güncel duyuru listesini çeker."""
    try:
        response = requests.get(f"{BASE_URL}/announcements", timeout=5)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        print(f"HATA (Duyuru Çekme): {e}")
        return []

def post_announcement(title: str, content: str):
    """Personel panelinden gelen yeni duyuruyu API'ye gönderir."""
    payload = {
        "baslik": title,
        "icerik": content,
        "etiket": "YENİ",
        "renk": "#3b82f6"
    }
    try:
        response = requests.post(f"{BASE_URL}/announcements", json=payload, timeout=5)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# 2. YEMEK MENÜSÜ İŞLEMLERİ (GET & PUT)
# ---------------------------------------------------------

def get_meal_menu():
    """FastAPI'den günün yemek menüsü metnini çeker."""
    try:
        response = requests.get(f"{BASE_URL}/meal-menu", timeout=5)
        response.raise_for_status()
        return response.json().get("menu", "Menü bilgisi alınamadı.")
    except Exception as e:
        print(f"HATA (Menü Çekme): {e}")
        return "Yemek listesi şu an yüklenemiyor."

def update_meal_api(new_menu: str):
    """Personel tarafından güncellenen menü metnini API'ye iletir."""
    try:
        # Menü metnini query parameter (sorgu parametresi) olarak gönderiyoruz
        response = requests.put(
            f"{BASE_URL}/meal-menu", 
            params={"menu_text": new_menu}, 
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# 2. AYLIK YEMEK MENÜSÜ İŞLEMLERİ


def get_monthly_meal_menu():
    try:
        response = requests.get(f"{BASE_URL}/monthly-meal-menu", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Aylık Menü Çekme): {e}")
        return {}


def save_monthly_meal_menu(menu_data: dict):
    try:
        response = requests.put(
            f"{BASE_URL}/monthly-meal-menu",
            json={"menu": menu_data},
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# 3. ARIZA BİLDİRİM İŞLEMLERİ (POST, GET & PUT)
# ---------------------------------------------------------

# services/api_service.py içindeki ilgili fonksiyonu bununla değiştir:

def send_fault_report(baslik: str, detay: str, oda_no: str, ogrenci_no: str):
    """Öğrencinin oluşturduğu arıza bildirimini API'ye kaydeder."""
    payload = {
        "baslik": baslik,
        "detay": detay,
        "oda_no": oda_no,
        "ogrenci_no": ogrenci_no  # ARTIK ÖĞRENCİ NUMARASI DA GİDİYOR!
    }
    try:
        response = requests.post(f"{BASE_URL}/report-fault", json=payload, timeout=5)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        return {"status": "error", "message": f"Sunucu hatası: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Bağlantı hatası: {str(e)}"}
def get_all_faults():
    """Sistemdeki tüm arıza kayıtlarını personel paneli için çeker."""
    try:
        response = requests.get(f"{BASE_URL}/faults", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Arıza Listesi): {e}")
        return []
    
def get_student_faults(student_number: str):
    """Belirli bir öğrenciye ait arızaları API'den (veritabanından) çeker."""
    try:
        # FastAPI'de bu endpoint'in (uç noktanın) olması gerekir
        response = requests.get(f"{BASE_URL}/student-faults/{student_number}", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Öğrenci Arıza Çekme): {e}")
        return []

def update_fault_api(fault_id: int, status: str):
    """Mevcut bir arızanın durumunu (Çözüldü/Beklemede vb.) günceller."""
    try:
        response = requests.put(
            f"{BASE_URL}/update-fault/{fault_id}", 
            params={"yeni_durum": status}, 
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    # services/api_service.py dosyasının en altına ekle:

def delete_fault_api(fault_id: int):
    """Personel panelinden gelen silme isteğini API'ye iletir."""
    try:
        response = requests.delete(f"{BASE_URL}/delete-fault/{fault_id}", timeout=5)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_student_api(username: str, password: str, full_name: str, room_no: str):
    """Öğrenci ekleme isteğini backend API'ye gönderir."""
    payload = {
        "username": username,
        "password": password,
        "full_name": full_name,
        "room_no": room_no
    }

    try:
        response = requests.post(f"{BASE_URL}/students/create", json=payload, timeout=5)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}