import requests

# Pushcut Webhook URL'in (senin verdiğin doğru URL kullanıldı)
PUSHCUT_API_URL = "https://api.pushcut.io/YOUR_PUSH_CUT_WEBHOOK"

# Anahtar kelimeler
ANAHTAR_KELIMELER = ["bolu", "kiralık", "satılık"]

# Kontrol edilecek siteler
SITELER = {
    "Bolu Belediyesi İlan Kontrolü": "https://www.bolu.bel.tr/category/kiralamavesatisihaleleri",
    "OİB İlan Kontrolü": "https://www.oib.gov.tr/ihaleler",
    "e-İhale İlan Kontrolü": "https://esatis.uyap.gov.tr/main.jsp",
    "Milli Emlak İlan Kontrolü": "https://www.milliemlak.gov.tr/ihale-ilanlari"
}

def bildirim_gonder(baslik, mesaj):
    try:
        response = requests.post(PUSHCUT_API_URL, json={"title": baslik, "text": mesaj})
        response.raise_for_status()
    except Exception as e:
        print(f"Pushcut bildirimi gönderilemedi: {e}")

def anahtar_kelime_var_mi(html):
    html_lower = html.lower()
    return any(anahtar in html_lower for anahtar in ANAHTAR_KELIMELER)

def site_kontrol_et():
    for site_adi, site_url in SITELER.items():
        try:
            response = requests.get(site_url, timeout=10)
            response.raise_for_status()
            if anahtar_kelime_var_mi(response.text):
                mesaj = f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulundu!"
            else:
                mesaj = f"{site_adi} sitesinde BOLU için kiralık veya satılık ilan bulunamadı."
        except Exception as e:
            mesaj = f"HATA: {site_url} sitesine ulaşılamadı."

        bildirim_gonder(site_adi, mesaj)

if __name__ == "__main__":
    site_kontrol_et()
