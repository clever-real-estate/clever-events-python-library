from abc import ABC, abstractmethod


class QueueBaseAdapter(ABC):

    @abstractmethod
    def fetch_messages(self, queue_name, max_number_of_messages=1):
        pass

    @abstractmethod
    def delete_message(self, queue_name, message_id):
        pass
