import requests
from bs4 import BeautifulSoup

# Bildirim gonderme fonksiyonu
def pushcut_bildirim(mesaj):
    url = "https://api.pushcut.io/YOUR_REAL_WEBHOOK_URL_HERE"  # Senin gerçek Pushcut URL'in burada
    headers = {"Content-Type": "application/json"}
    data = {"text": mesaj}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Pushcut bildirimi gönderilemedi: {e}")

# Siteleri ve anahtar kelimeleri kontrol etme fonksiyonu
def siteyi_kontrol_et(site_adi, site_url, anahtar_kelimeler):
    try:
        response = requests.get(site_url, timeout=15)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        metin = soup.get_text().lower()

        if any(kelime in metin for kelime in anahtar_kelimeler):
            pushcut_bildirim(f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulundu!")
        else:
            pushcut_bildirim(f"{site_adi} sitesinde Bolu için kiralık veya satılık ilan bulunamadı.")
    except Exception as e:
        pushcut_bildirim(f"HATA: {site_url} sitesine ulaşılamadı. {e}")

# Ana fonksiyon
def main():
    anahtar_kelimeler = ["bolu", "kiralık", "satılık"]

    siteler = [
        ("Bolu Belediyesi", "https://www.bolu.bel.tr/duyurular"),
        ("OİB", "https://www.oib.gov.tr/ihaleler"),
        ("e-İhale", "https://www.eihale.gov.tr/"),
        ("Milli Emlak", "https://www.milliemlak.gov.tr/ihale-ilanlari"),
        ("TOKİ", "https://www.toki.gov.tr/duyurular")
    ]

    for site_adi, site_url in siteler:
        siteyi_kontrol_et(site_adi, site_url, anahtar_kelimeler)

if __name__ == "__main__":
    main()
