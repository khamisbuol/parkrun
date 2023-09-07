class Event:

    LATEST_RESULTS = "latest_results"
    ATTENDANCE_RECORDS = "attendance_records"
    EVENT_HISTORY = "event_history"
    SINGLE_EVENT = "single_event"

    def __init__(self, event_type: str) -> None:
        self.event_type = event_type
        pass
