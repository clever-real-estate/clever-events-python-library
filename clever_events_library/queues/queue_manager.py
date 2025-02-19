from .adapters import QueueBaseAdapter


class QueueManager:
    def __init__(self, queue_adapter: QueueBaseAdapter):
        self.queue_adapter = queue_adapter

    def fetch_messages(self, queue_name, max_number_of_messages=1):
        return self.queue_adapter.fetch_messages(queue_name, max_number_of_messages)

    def delete_message(self, queue_name, message_id):
        return self.queue_adapter.delete_message(queue_name, message_id)
