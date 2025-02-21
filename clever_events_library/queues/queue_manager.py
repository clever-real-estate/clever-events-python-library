from collections.abc import Iterator

from .adapters import QueueBaseAdapter


class QueueManager:
    def __init__(self, queue_adapter: QueueBaseAdapter) -> None:
        """
        Initialize QueueManager with queue_adapter

        Args:
            queue_adapter (QueueBaseAdapter): An instance of QueueBaseAdapter

        Returns:
            None
        """
        self.queue_adapter = queue_adapter

    def fetch_messages(self, queue_name: str, max_number_of_messages: int = 1) -> Iterator[dict]:
        """
        Fetch messages from the queue

        Args:
            queue_name (str): The name of the queue
            max_number_of_messages (int, optional): Highest number of messages we want to fetch. Defaults to 1.

        Yields:
            Iterator[dict]: A generator that yields messages from the queue
        """
        return self.queue_adapter.fetch_messages(queue_name, max_number_of_messages)

    def delete_message(self, queue_name: str, message_id: str) -> dict:
        """
        Delete a message from the queue

        Args:
            queue_name (str): The name of the queue
            message_id (str): The id of the message we want to delete

        Returns:
            dict: A dict containing the response we got from the stack when performing deletion
        """
        return self.queue_adapter.delete_message(queue_name, message_id)
