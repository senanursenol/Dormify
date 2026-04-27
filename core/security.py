def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    DİKKAT: Geçici olarak şifreleme kapalı!
    Gelen şifre ile veritabanındaki şifreyi doğrudan düz metin olarak eşleştirir.
    Örn: "123456" == "123456"
    """
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """
    DİKKAT: Geçici olarak şifreleme kapalı!
    Yeni şifre oluşturulurken şifreyi değiştirmeden aynen veritabanına kaydeder.
    """
    return password