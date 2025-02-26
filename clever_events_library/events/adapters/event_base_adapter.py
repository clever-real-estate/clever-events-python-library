from abc import ABC, abstractmethod


class EventBaseAdapter(ABC):

    @abstractmethod
    def sync_publish(self, event_name: str, message_data: dict) -> None:
        """
        Syncronously publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def async_publish(self, event_name: str, message_data: dict) -> None:
        """
        Asynchronously publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.

        Returns:
            None
        """
        pass
