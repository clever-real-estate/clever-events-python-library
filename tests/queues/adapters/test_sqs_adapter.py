import json
from unittest import TestCase
from unittest.mock import MagicMock, patch

from clever_events_library.queues.adapters.sqs_adapter import SQSAdapter


class TestSQSAdapter(TestCase):
    def setUp(self):
        self.client_config = {
            "aws_region": "us-east-1",
            "aws_account_id": "123456789012",
            "aws_key": "fake_key",
            "aws_secret": "fake_secret",
        }
        self.sqs_adapter = SQSAdapter(client_config=self.client_config)

    @patch("boto3.client")
    def test_sqs_client_initialization(self, mock_boto_client):
        self.sqs_adapter.sqs_client
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
                    "ReceiptHandle": "handle1",
                    "Body": json.dumps({"key": "value"}),
                    "MessageAttributes": {}
                }
            ]
        }

        messages = list(self.sqs_adapter.fetch_messages("test_queue"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["message_id"], "1")
        self.assertEqual(messages[0]["message_data"], {"key": "value"})

    @patch("boto3.client")
    def test_delete_message(self, mock_boto_client):
        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client
        mock_sqs_client.delete_message.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        response = self.sqs_adapter.delete_message("test_queue", "handle1")
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    @patch("boto3.client")
    def test_get_queue_url(self, mock_boto_client):
        expected_url = f"https://sqs.{self.client_config['aws_region']}.amazonaws.com/{self.client_config['aws_account_id']}/test_queue"
        queue_url = self.sqs_adapter._get_queue_url("test_queue")
        self.assertEqual(queue_url, expected_url)
