from unittest import TestCase
from unittest.mock import MagicMock

from clever_events_library.queues.adapters import QueueBaseAdapter
from clever_events_library.queues.queue_manager import QueueManager


class TestQueueManager(TestCase):
    def setUp(self):
        self.mock_adapter = MagicMock(spec=QueueBaseAdapter)
        self.queue_manager = QueueManager(self.mock_adapter)

    def test_fetch_messages(self):
        queue_name = "test_queue"
        max_number_of_messages = 5
        expected_messages = ["message1", "message2"]

        self.mock_adapter.fetch_messages.return_value = expected_messages

        messages = self.queue_manager.fetch_messages(queue_name, max_number_of_messages)

        self.mock_adapter.fetch_messages.assert_called_once_with(
            queue_name, max_number_of_messages
        )
        self.assertEqual(messages, expected_messages)

    def test_delete_message(self):
        queue_name = "test_queue"
        message_id = "message1"
        expected_result = True

        self.mock_adapter.delete_message.return_value = expected_result

        result = self.queue_manager.delete_message(queue_name, message_id)

        self.mock_adapter.delete_message.assert_called_once_with(queue_name, message_id)
        self.assertEqual(result, expected_result)
