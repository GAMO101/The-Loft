import scrapy
import json
from datetime import date
from dateutil import parser

# Get today's date
today = date.today().strftime('%Y-%m-%d')

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = [
        'https://www.theloft.at/'
    ]
    print(start_urls)

    # Custom settings for the spider
    custom_settings = {
        'FEEDS': {
            'loft.json': {
                'format': 'json',
                'overwrite': True,  # If the file already exists, it will overwrite it
                'indent': 4,  # Better readable
            },
        },
    }

    def parse(self, response):
        # Extraction of date, open time, title, location, and links
        date_info = response.xpath('//div[contains(@class, "datum")]/text()').getall()
        open_time = response.xpath('//span[contains(@class, "open")]/text()').getall()
        event_titles = response.xpath('//div[contains(@class, "content-middle")]/text()').getall()
        event_locations = response.xpath('//div[contains(@class, "content-right")]/text()').getall()
        event_links = response.xpath('//div[contains(@class, "elementor-shortcode")]//a/@href').getall()

        self.log(f"Extracted date info: {date_info}")
        self.log(f"Extracted event titles: {event_titles}")
        self.log(f"Extracted event locations: {event_locations}")
        self.log(f"Extracted open times: {open_time}")
        self.log(f"Extracted event links: {event_links}")

        # Ensure the lists are of the same length
        if not (len(date_info) == len(event_titles) == len(event_locations) == len(open_time) == len(event_links)):
            self.log("Warning: The number of dates, event titles, locations, open times, and links do not match!")

        events = []
        for date_str, open_str, title, location, link in zip(date_info, open_time, event_titles, event_locations, event_links):
            try:
                event_date = parser.parse(date_str, dayfirst=True, fuzzy=True).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                event_date = "Unknown"

            # Append event with title, date, location, open time, and link
            events.append({
                'title': title.strip() if title else 'No Title',
                'date': event_date,
                'open': open_str.strip() if open_str else 'No Open Time',
                'location': location.strip() if location else 'No Location',
                'link': link.strip() if link else 'No Link'
            })

        yield {
            'events': events
        }
