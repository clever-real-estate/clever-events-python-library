from abc import ABC, abstractmethod


class EventBaseAdapter(ABC):

    @abstractmethod
    def publish(self, event_name: str, message_data: dict) -> None:
        """
        Publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.

        Returns:
            None
        """
        pass
