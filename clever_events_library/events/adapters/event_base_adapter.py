from abc import ABC, abstractmethod


class EventBaseAdapter(ABC):

    @abstractmethod
    def sync_publish(
        self, event_name: str, message_data: dict, additional_params: dict = {}
    ) -> None:
        """
        Syncronously publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.
            additional_params (dict): A dict containing additional parameters to be sent in the events stack call. It is optional.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def async_publish(
        self, event_name: str, message_data: dict, additional_params: dict = {}
    ) -> None:
        """
        Asynchronously publish an event to the event stack

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message attributes.
            additional_params (dict): A dict containing additional parameters to be sent in the events stack call. It is optional.

        Returns:
            None
        """
        pass
