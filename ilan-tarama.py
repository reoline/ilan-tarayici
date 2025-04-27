import requests

# Pushcut Webhook URL
PUSHCUT_API_URL = "https://api.pushcut.io/CLDonSTvi22mteRYjxTdI/notifications/Milli%20Emlak"

def send_pushcut_notification(text):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }
    try:
        response = requests.post(PUSHCUT_API_URL, headers=headers, json=data)
        response.raise_for_status()
        print(f"Bildirim gönderildi: {text}")
    except Exception as e:
        print(f"HATA: Bildirim gönderilemedi: {e}")

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"HATA: {url} sitesine ulaşılamadı.")
        send_pushcut_notification(f"{url} sitesine ulaşılamadı.")
        return None

def kontrol_et(url, site_adi):
    html = fetch_html(url)
    if html:
        html_lower = html.lower()
        if "bolu" in html_lower and ("kiralık" in html_lower or "satılık" in html_lower):
            send_pushcut_notification(f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulundu!")
        else:
            send_pushcut_notification(f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulunamadı.")

def main():
    siteler = {
        "Milli Emlak": "https://www.milliemlak.gov.tr",
        "e-İhale": "https://www.eihale.gov.tr",
        "Toki": "https://www.toki.gov.tr",
        "OİB": "https://www.oib.gov.tr",
        "Vakıflar Genel Müdürlüğü": "https://www.vgm.gov.tr",
        "Bolu Belediyesi": "https://www.bolu.bel.tr/category/kiralamavesatisihaleleri"
    }

    for site_adi, url in siteler.items():
        kontrol_et(url, site_adi)

if __name__ == "__main__":
    main()
