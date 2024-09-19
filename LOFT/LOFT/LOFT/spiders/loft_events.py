import json
import requests
from datetime import datetime

# Načítanie JSON súboru
with open('loft.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Skontrolujeme, či je načítaný súbor zoznam a získame prvý prvok
if isinstance(data, list) and len(data) > 0:
    first_item = data[0]  # Prvý prvok zoznamu

    # Získanie údajov o eventoch
    events = first_item.get('events', [])

    # Tvoj Telegram bot token
    token = '7162097876:AAE27cvUGt6tUzuX3NI9VoNnoUsbNYYnBUM'
    method = "sendMessage"
    chat_id = -1002278281776  # ID Telegram skupiny

    # Inicializácia prázdneho zoznamu pre uloženie neúspešných odoslaní
    failed_events = []

    # Získanie dnešného dátumu v tvare 'YYYY-MM-DD'
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Spracovanie každého eventu
    for event in events:
        title = event.get('title', 'No Title')
        event_date = event.get('date', 'No Date').strip()  # Očakávame dátum vo formáte 'YYYY-MM-DD'

        location = event.get('location', 'No Location')
        open_time = event.get('open', 'No Open Time')
        link = event.get('link', 'No Link')

        # Skontrolujeme, či sa event koná dnes porovnaním dátumu udalosti s dnešným dátumom
        if event_date == today_date:
            # Kombinovaná správa s názvom, dátumom, miestom, časom a odkazom
            message = f"🎉 Event: {title}\n📅 Date: {event_date}\n📍 Location: {location}\n⏰ Time: {open_time}\n🔗 Link: {link}"

            # Pošleme správu pomocou Telegram API
            response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={
                'chat_id': chat_id,
                'text': message
            })

            # Skontrolujeme, či bola správa úspešne odoslaná
            if response.status_code != 200:
                failed_events.append(title)  # Pridáme názov eventu do zoznamu neúspešných

    # Výpis neúspešných odoslaní (ak nejaké sú)
    if failed_events:
        print("Failed to send messages for the following events:")
        for failed in failed_events:
            print(failed)
    else:
        print("All messages for today's events were successfully sent!")

else:
    print("The JSON structure is not as expected or the list is empty.")