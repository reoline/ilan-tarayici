import requests
from bs4 import BeautifulSoup
import os

# Pushcut API URL'in
PUSHCUT_API_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Milli%20Emlak"

# Bildirim gönderen fonksiyon
def send_pushcut_notification(title, message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "text": message
    }
    try:
        response = requests.post(PUSHCUT_API_URL, headers=headers, json=data)
        response.raise_for_status()
        print(f"Bildirim gönderildi: {title} - {message}")
    except Exception as e:
        print(f"HATA: Bildirim gönderilemedi: {e}")

# Site çekim fonksiyonu
def check_site(site_name, url, keyword):
    try:
        print(f"{site_name} kontrol ediliyor...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        print(f"HATA: {site_name} sitesine ulaşılamadı: {e}")
        send_pushcut_notification(f"{site_name} - HATA", f"{site_name} sitesine ulaşılamadı.")
        return

    soup = BeautifulSoup(html_content, "html.parser")

    if keyword.lower() in soup.text.lower():
        send_pushcut_notification(f"{site_name} İlan Bulundu!", f"{site_name} sitesinde {keyword} anahtar kelimesi bulundu!")
    else:
        send_pushcut_notification(f"{site_name} İlan Kontrolü", f"{site_name} sitesinde {keyword} anahtar kelimesi bulunamadı.")

# Ana fonksiyon
def main():
    sites = [
        {
            "name": "Milli Emlak",
            "url": "https://www.milliemlak.gov.tr/",
            "keyword": "bolu"
        },
        {
            "name": "e-İhale",
            "url": "https://www.eihale.gov.tr/",
            "keyword": "bolu"
        },
        {
            "name": "OİB",
            "url": "https://www.oib.gov.tr/",
            "keyword": "bolu"
        },
        {
            "name": "Bolu Belediyesi",
            "url": "https://www.bolu.bel.tr/category/kiralamavesatisihaleleri",
            "keyword": "bolu"
        },
        {
            "name": "İlan.gov.tr",
            "url": "https://www.ilan.gov.tr/",
            "keyword": "bolu"
        }
    ]

    for site in sites:
        check_site(site["name"], site["url"], site["keyword"])

if __name__ == "__main__":
    main()
