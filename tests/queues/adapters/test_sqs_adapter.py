import json
import unittest
from unittest.mock import MagicMock, patch

from clever_events_library.queues.adapters.sqs_adapter import SQSAdapter


class TestSQSAdapter(unittest.TestCase):

    def setUp(self):
        self.client_config = {
            "aws_region": "us-east-1",
            "aws_account_id": "123456789012",
            "aws_key": "fake_key",
            "aws_secret": "fake_secret",
            "await_time": 10,
        }
        self.sqs_adapter = SQSAdapter(self.client_config)

    @patch("boto3.client")
    def test_sqs_client_initialization(self, mock_boto_client):
        mock_boto_client.return_value = MagicMock()
        client = self.sqs_adapter.sqs_client
        self.assertIsNotNone(client)
        mock_boto_client.assert_called_once_with(
            "sqs",
            region_name=self.client_config["aws_region"],
            aws_access_key_id=self.client_config["aws_key"],
            aws_secret_access_key=self.client_config["aws_secret"],
        )

    @patch("boto3.client")
    def test_fetch_messages(self, mock_boto_client):
        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client
        mock_sqs_client.receive_message.return_value = {
            "Messages": [
                {
                    "MessageId": "1",
                    "ReceiptHandle": "abc",
                    "Body": json.dumps(
                        {"Message": json.dumps({"key": "value"}), "MessageAttributes": {}}
                    ),
                },
                {
                    "MessageId": "5",
                    "ReceiptHandle": "cba",
                    "Body": json.dumps(
                        {"Message": json.dumps({"key": "value"}), "MessageAttributes": {}}
                    ),
                },
            ]
        }

        messages = self.sqs_adapter.fetch_messages("test_queue")
        count = 0
        message_ids = []
        for message in messages:
            self.assertIsNotNone(message)
            count += 1
            message_ids.append(message["message_id"])
        self.assertEqual(message_ids, ["1", "5"])
        self.assertEqual(count, 2)

    @patch("boto3.client")
    def test_delete_message(self, mock_boto_client):
        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client

        self.sqs_adapter.delete_message("test_queue", "abc")
        mock_sqs_client.delete_message.assert_called_once_with(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/123456789012/test_queue",
            ReceiptHandle="abc",
        )

    def test_validate_client_config(self):
        with self.assertRaises(ValueError):
            SQSAdapter({})

    def test_get_queue_url(self):
        queue_url = self.sqs_adapter._get_queue_url("test_queue")
        self.assertEqual(queue_url, "https://sqs.us-east-1.amazonaws.com/123456789012/test_queue")
