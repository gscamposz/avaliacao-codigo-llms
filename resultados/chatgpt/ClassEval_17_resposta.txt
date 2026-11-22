from datetime import datetime, timedelta


class CalendarUtil:
    """
    This is a class as CalendarUtil that provides functionalities
    to manage calendar events, schedule appointments, and perform
    conflict checks.
    """

    def __init__(self):
        """
        Initialize the calendar with an empty list of events.
        """
        self.events = []

    def add_event(self, event):
        """
        Add an event to the calendar.
        :param event: dict
        """
        self.events.append(event)

    def remove_event(self, event):
        """
        Remove an event from the calendar.
        :param event: dict
        """
        if event in self.events:
            self.events.remove(event)

    def get_events(self, date):
        """
        Get all events on a given date.
        :param date: datetime
        :return: list
        """
        return [
            event
            for event in self.events
            if event["date"].date() == date.date()
        ]

    def is_available(self, start_time, end_time):
        """
        Check if the calendar is available for a given time slot.
        :param start_time: datetime
        :param end_time: datetime
        :return: bool
        """
        if start_time >= end_time:
            return False

        for event in self.events:
            event_start = event.get("start_time", event["date"])
            event_end = event.get("end_time", event_start)

            if start_time < event_end and end_time > event_start:
                return False

        return True

    def get_available_slots(self, date):
        """
        Get all available time slots on a given date.
        :param date: datetime
        :return: list
        """
        day_start = datetime.combine(date.date(), datetime.min.time())
        day_end = day_start + timedelta(days=1)

        busy_slots = []

        for event in self.events:
            event_start = event.get("start_time", event["date"])
            event_end = event.get("end_time", event_start)

            if event_start < day_end and event_end > day_start:
                busy_start = max(event_start, day_start)
                busy_end = min(event_end, day_end)

                if busy_start < busy_end:
                    busy_slots.append((busy_start, busy_end))

        busy_slots.sort(key=lambda slot: slot[0])

        available_slots = []
        current_time = day_start

        for busy_start, busy_end in busy_slots:
            if current_time < busy_start:
                available_slots.append((current_time, busy_start))

            current_time = max(current_time, busy_end)

        if current_time < day_end:
            available_slots.append((current_time, day_end))

        return available_slots

    def get_upcoming_events(self, num_events):
        """
        Get the next n upcoming events.
        :param num_events: int
        :return: list
        """
        sorted_events = sorted(
            self.events,
            key=lambda event: event["date"]
        )

        return [
            event
            for event in sorted_events
            if event["date"] >= datetime.now()
        ][:num_events]