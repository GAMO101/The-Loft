import json
import requests

# Načítanie JSON súboru
with open('dataClean2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Skontrolujeme, či je načítaný súbor zoznam a získame prvý prvok
if isinstance(data, list) and len(data) > 0:
    first_item = data[0]  # Prvý prvok zoznamu

    # Získanie údajov o eventoch
    events = first_item.get('events', [])

    # Tvoj Telegram bot token
    token = '6928160486:AAFwy-vcEhLiUw6_mWDaykPBn90evij-WOM'
    method = "sendMessage"
    chat_id = -1002381362019  # ID Telegram skupiny

    # Inicializácia prázdneho zoznamu pre uloženie neúspešných odoslaní
    failed_events = []

    # Spracovanie každého eventu
    for event in events:
        title = event.get('title', 'No Title')  # Ošetríme chýbajúce kľúče
        event_date = event.get('date', 'No Date')
        location = event.get('location', 'No Location')
        open_time = event.get('open', 'No Open Time')
        link = event.get('link', 'No Link')

        # Kombinovaná správa s názvom, dátumom, miestom, časom a odkazom
        message = f"Title: {title}\nDate: {event_date}\nLocation: {location}\nOpen: {open_time}\nLink: {link}"

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
        print("All messages were successfully sent!")

else:
    print("The JSON structure is not as expected or the list is empty.")