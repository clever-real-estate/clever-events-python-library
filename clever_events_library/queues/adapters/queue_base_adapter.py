from abc import ABC, abstractmethod
from collections.abc import Iterator


class QueueBaseAdapter(ABC):

    @abstractmethod
    def fetch_messages(self, queue_name: str, max_number_of_messages: int = 1) -> Iterator[dict]:
        """
        Fetch messages from the queue

        Args:
            queue_name (str): The name of the queue
            max_number_of_messages (int, optional): Highest number of messages we want to fetch. Defaults to 1.

        Yields:
            Iterator[dict]: A generator that yields messages from the queue
        """
        pass

    @abstractmethod
    def delete_message(self, queue_name: str, message_id: str) -> dict:
        """
        Delete a message from the queue

        Args:
            queue_name (str): The name of the queue
            message_id (str): The id of the message we want to delete

        Returns:
            dict: A dict containing the response we got from the stack when performing deletion
        """
        pass
