

import requests

class NaturalEvent:
    def __init__(
            self,
            eonet_id,
            title,
            category,
            status,
            latitude,
            longitude,
            event_date,
            magnitude,
            mag_unit,
            source_url
    ):
        self.__eonet_id = eonet_id
        self.title = title
        self.category = category
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.event_date = event_date
        self.magnitude = magnitude
        self.mag_unit = mag_unit
        self.source_url = source_url

    @property
    def eonet_id(self):
        return self.__eonet_id

    def is_active(self):
        return self.status == "open"

    def summary(self):
        return f"{self.category} | {self.title} | {self.status}"


class WatchedEvent(NaturalEvent):
    def __init__(
            self,
            eonet_id,
            title,
            category,
            status,
            latitude,
            longitude,
            event_date,
            magnitude,
            mag_unit,
            source_url,
            note = "",
            alert_active = False
        ):
        super().__init__(
            eonet_id,
            title,
            category,
            status,
            latitude,
            longitude,
            event_date,
            magnitude,
            mag_unit,
            source_url
        )

        self.note = note
        self.alert_active = alert_active

    def toggle_alert(self):
        self.alert_active = not self.alert_active
        return self.alert_active

    def summary(self):
        base_summary = super().summary()

        return f"{base_summary} | Note: {self.note} | Alert: {self.alert_active}"




class EventFetcher:
    BASE_URL = "https://eonet.gsfc.nasa.gov/api/v3"

    def fetch_events(self, status = "open", category = None, days = 30, limit = 20):
        params = {
            "status": status,
            "days": days,
            "limit": limit
        }

        if category:
            params["category"] = category

        response = requests.get(
            f"{self.BASE_URL}/events",
            params = params,
            timeout = 10
        )

        response.raise_for_status()

        data = response.json()

        events = []

        for item in data["events"]:
            category = item["categories"][0]["title"]

            geometry = item["geometry"][0]
            longitude = geometry["coordinates"][0]
            latitude = geometry["coordinates"][1]

            event_date = geometry["date"][:10]

            status = "open" if item["closed"] is None else "closed"

            source_url = item["sources"][0]["url"]

            event = NaturalEvent(
                item["id"],
                item["title"],
                category,
                status,
                latitude,
                longitude,
                event_date,
                None,
                None,
                source_url
            )

            events.append(event)

        return events

    def fetch_event(self, eonet_id):
        response = requests.get(
            f"{self.BASE_URL}/events/{eonet_id}",
            timeout = 10
        )

        response.raise_for_status()

        item = response.json()

        category = item["categories"][0]["title"]

        geometry = item["geometry"][0]
        longitude = geometry["coordinates"][0]
        latitude = geometry["coordinates"][1]

        event_date = geometry["date"][:10]

        status = "open" if item["closed"] is None else "closed"

        source_url = item["sources"][0]["url"]

        magnitude = geometry.get("magnitudeValue")
        mag_unit = geometry.get("magnitudeUnit")

        return NaturalEvent(
            item["id"],
            item["title"],
            category,
            status,
            latitude,
            longitude,
            event_date,
            magnitude,
            mag_unit,
            source_url
        )


    def fetch_categories(self):
        response = requests.get(
            f"{self.BASE_URL}/categories",
            timeout = 10
        )

        response.raise_for_status()

        data = response.json()

        return data["categories"]