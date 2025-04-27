import requests
import time

PUSHCUT_API_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Milli%20Emlak"

SITES = [
    ("Milli Emlak", "https://www.milliemlak.gov.tr"),
    ("e-İhale", "https://www.eihale.gov.tr"),
    ("OİB", "https://www.oib.gov.tr"),
    ("TOKİ", "https://www.toki.gov.tr"),
    ("Bolu Belediyesi", "https://www.bolu.bel.tr/category/kiralamavesatisihaleleri"),
]

KEYWORDS = ["bolu", "kiralık", "satılık"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                return None

def send_pushcut_notification(title, message):
    data = {"title": title, "text": message}
    try:
        response = requests.post(PUSHCUT_API_URL, json=data)
        response.raise_for_status()
        print(f"Bildirim gönderildi: {title}")
    except Exception as e:
        print(f"HATA: Bildirim gönderilemedi. {e}")

def kontrol_et():
    for site_adi, site_url in SITES:
        print(f"{site_adi} kontrol ediliyor...")
        html = fetch_page(site_url)
        
        if html is None:
            send_pushcut_notification(
                f"{site_adi} - HATA",
                f"{site_url} sitesine ulaşılamadı."
            )
            continue

        html_lower = html.lower()
        if any(keyword in html_lower for keyword in KEYWORDS):
            send_pushcut_notification(
                f"{site_adi} İlan Bulundu!",
                f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulundu!"
            )
        else:
            send_pushcut_notification(
                f"{site_adi} İlan Kontrolü",
                f"{site_adi} sitesinde Bolu için kiralık veya satılık ilan bulunamadı."
            )

if __name__ == "__main__":
    kontrol_et()