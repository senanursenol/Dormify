import requests
import streamlit as st
import base64

# FastAPI sunucusunun çalıştığı adres ve port
BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------
# 1. DUYURU İŞLEMLERİ (GET & POST)
# ---------------------------------------------------------

def get_announcements():
    """FastAPI'den tüm güncel duyuru listesini çeker."""
    try:
        response = requests.get(f"{BASE_URL}/announcements", timeout=20)
        response.raise_for_status() 
        return response.json()
    except Exception as e:
        print(f"HATA (Duyuru Çekme): {e}")
        return []

def post_announcement(title: str, content: str, gorsel=None):
    """Personel panelinden gelen yeni duyuruyu API'ye gönderir."""
    payload = {
        "baslik": title,
        "icerik": content,
        "etiket": "YENİ",
        "renk": "#3b82f6"
    }
    
    # Görsel varsa base64'e çevir
    if gorsel is not None:
        try:
            image_bytes = gorsel.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            payload["gorsel"] = encoded_image
        except Exception as e:
            print(f"Görsel okuma hatası: {e}")
        
    try:
        response = requests.post(f"{BASE_URL}/announcements", json=payload, timeout=20)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
# ---------------------------------------------------------
# 2. YEMEK MENÜSÜ İŞLEMLERİ (GET & PUT)
# ---------------------------------------------------------

@st.cache_data(ttl=60)
def get_meal_menu():
    """FastAPI'den günün yemek menüsü metnini çeker."""
    try:
        response = requests.get(f"{BASE_URL}/meal-menu", timeout=20)
        response.raise_for_status()
        return response.json().get("menu", "Menü bilgisi alınamadı.")
    except Exception as e:
        print(f"HATA (Menü Çekme): {e}")
        return "Yemek listesi şu an yüklenemiyor."

@st.cache_data(ttl=60)
def get_breakfast_menu():
    """FastAPI'den günün kahvaltı menüsü metnini çeker."""
    try:
        response = requests.get(f"{BASE_URL}/breakfast-menu", timeout=20)
        response.raise_for_status()
        return response.json().get("menu", "Kahvaltı menüsü bilgisi alınamadı.")
    except Exception as e:
        print(f"HATA (Kahvaltı Menü Çekme): {e}")
        return "Kahvaltı menüsü şu an yüklenemiyor."

def update_meal_api(new_menu: str):
    """Personel tarafından güncellenen menü metnini API'ye iletir."""
    try:
        # Menü metnini query parameter (sorgu parametresi) olarak gönderiyoruz
        response = requests.put(
            f"{BASE_URL}/meal-menu",
            params={"menu_text": new_menu},
            timeout=20
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# AYLIK YEMEK MENÜSÜ İŞLEMLERİ
# ---------------------------------------------------------

@st.cache_data(ttl=60)
def get_monthly_meal_menu():
    try:
        response = requests.get(f"{BASE_URL}/monthly-meal-menu", timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Aylık Menü Çekme): {e}")
        return {}

@st.cache_data(ttl=60)
def get_monthly_breakfast_menu():
    try:
        response = requests.get(f"{BASE_URL}/monthly-breakfast-menu", timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Aylık Kahvaltı Menü Çekme): {e}")
        return {}

def save_monthly_meal_menu(payload: dict):
    """Aylık menü paketini (yıl, ay ve günler) FastAPI'ye fırlatır."""
    try:
        response = requests.post(f"{BASE_URL}/save-monthly-menu", json=payload, timeout=20)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------------------------------------------------
# 3. ARIZA BİLDİRİM İŞLEMLERİ (POST, GET, PUT & DELETE)
# ---------------------------------------------------------

def send_fault_report(baslik: str, detay: str, ogrenci_no: str, gorsel=None):
    """Öğrencinin oluşturduğu arıza bildirimini API'ye kaydeder. Oda no otomatik bulunur."""
    payload = {
        "baslik": baslik,
        "detay": detay,
        "ogrenci_no": ogrenci_no 
    }
    
    # Görsel varsa base64'e çevir ve payload'a ekle
    if gorsel is not None:
        image_bytes = gorsel.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        payload["gorsel"] = encoded_image
    
    try:
        response = requests.post(f"{BASE_URL}/report-fault", json=payload, timeout=20)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        return {"status": "error", "message": f"Sunucu hatası: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Bağlantı hatası: {str(e)}"}

@st.cache_data(ttl=60)
def get_all_faults():
    """Sistemdeki tüm arıza kayıtlarını personel paneli için çeker."""
    try:
        response = requests.get(f"{BASE_URL}/faults", timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HATA (Arıza Listesi): {e}")
        return []
    
def get_student_faults(student_number: str):
    try:
        print(f"📡 API'ye istek atılıyor: Öğrenci No: {student_number}")
        response = requests.get(f"{BASE_URL}/student-faults/{student_number}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📦 API'den Gelen Veri Sayısı: {len(data)}")
            print(f"🔍 Gelen Veri İçeriği: {data}") # Verinin içini görelim
            return data
        
        print(f"❌ API Hatası: {response.status_code}")
        return []
    except Exception as e:
        print(f"🔥 KURYEDE HATA: {e}")
        return []
def update_fault_api(fault_id: int, status: str):
    """Mevcut bir arızanın durumunu (Çözüldü/Beklemede vb.) günceller."""
    try:
        response = requests.put(
            f"{BASE_URL}/update-fault/{fault_id}", 
            params={"yeni_durum": status}, 
            timeout=20
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def delete_announcement_api(duyuru_id: int):
    """Personelin sildiği duyuruyu API'ye iletir."""
    try:
        response = requests.delete(f"{BASE_URL}/announcements/{duyuru_id}", timeout=20)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_fault_api(fault_id: int):
    """Personel panelinden gelen silme isteğini API'ye iletir."""
    try:
        response = requests.delete(f"{BASE_URL}/delete-fault/{fault_id}", timeout=20)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_fault_image_api(fault_id: int):
    """Sadece istenen arızanın görselini API'den çeker."""
    try:
        response = requests.get(f"{BASE_URL}/fault-image/{fault_id}", timeout=10)
        if response.status_code == 200:
            return response.json().get("gorsel")
        return None
    except Exception as e:
        print(f"HATA (Görsel Çekme): {e}")
        return None

# ---------------------------------------------------------
# 4. ÖĞRENCİ İŞLEMLERİ
# ---------------------------------------------------------

def create_student_api(username: str, password: str, full_name: str, room_no: str):
    """Öğrenci ekleme isteğini backend API'ye gönderir."""
    payload = {
        "username": username,
        "password": password,
        "full_name": full_name,
        "room_no": room_no
    }

    try:
        response = requests.post(f"{BASE_URL}/students/create", json=payload, timeout=20)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}