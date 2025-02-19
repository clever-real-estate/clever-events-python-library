from .adapters import EventBaseAdapter


class EventPublisher:
    def __init__(self, event_adapter: EventBaseAdapter):
        self.event_adapter = event_adapter

    def publish(self, event_name, message_data):
        self.event_adapter.publish(event_name, message_data)
