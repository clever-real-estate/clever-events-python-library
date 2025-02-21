from .adapters import EventBaseAdapter


class EventPublisher:
    def __init__(self, event_adapter: EventBaseAdapter) -> None:
        """
        Initialize EventPublisher with event_adapter

        Args:
            event_adapter (EventBaseAdapter): An instance of EventBaseAdapter

        Returns:
            None
        """
        self.event_adapter = event_adapter

    def publish(self, event_name: str, message_data: dict) -> None:
        """
        Publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.
        """
        self.event_adapter.publish(event_name, message_data)
