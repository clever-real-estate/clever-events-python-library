from abc import ABC, abstractmethod


class EventBaseAdapter(ABC):

    @abstractmethod
    def publish(self, event_name, message_data):
        pass
