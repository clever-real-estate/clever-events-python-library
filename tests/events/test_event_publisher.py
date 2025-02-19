import unittest
from unittest.mock import MagicMock

from clever_events_library.events.adapters import EventBaseAdapter, SNSAdapter
from clever_events_library.events.event_publisher import EventPublisher


class TestEventPublisher(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = MagicMock(spec=EventBaseAdapter)
        self.publisher = EventPublisher(self.mock_adapter)
        self.mock_sns_adapter = MagicMock(spec=SNSAdapter)
        self.sns_publisher = EventPublisher(self.mock_sns_adapter)

    def test_publish_calls_adapter_publish(self):
        event_name = "test_event"
        message_data = {"key": "value"}

        self.publisher.publish(event_name, message_data)

        self.mock_adapter.publish.assert_called_once_with(event_name, message_data)

    def test_publish_calls_sns_adapter_publish(self):
        event_name = "test_event"
        message_data = {"key": "value"}

        self.sns_publisher.publish(event_name, message_data)

        self.mock_sns_adapter.publish.assert_called_once_with(event_name, message_data)
