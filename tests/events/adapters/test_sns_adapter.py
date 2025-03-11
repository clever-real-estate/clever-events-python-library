import asyncio
from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from clever_events_library.events.adapters.sns_adapter import SNSAdapter


class TestSNSAdapter(TestCase):

    def setUp(self):
        self.client_config = {
            "aws_region": "us-east-1",
            "aws_key": "fake_key",
            "aws_secret": "fake_secret",
            "aws_account_id": "123456789012",
        }
        self.sns_adapter = SNSAdapter(client_config=self.client_config)

    @patch("boto3.client")
    def test_sns_client_initialization(self, mock_boto_client):
        self.assertIsNone(self.sns_adapter._sns_client)
        _ = self.sns_adapter.sns_client
        mock_boto_client.assert_called_once_with(
            "sns",
            region_name="us-east-1",
            aws_access_key_id="fake_key",
            aws_secret_access_key="fake_secret",
        )
        self.assertIsNotNone(self.sns_adapter._sns_client)

    @patch.object(
        SNSAdapter, "_get_topic_arn", return_value="arn:aws:sns:us-east-1:123456789012:my_topic"
    )
    def test_sync_publish(self, mock_get_topic_arn):
        message_data = {"message": {"key": "value"}, "message_attributes": {"attr1": "value1"}}
        self.sns_adapter.sns_client.publish = MagicMock()
        self.sns_adapter.sync_publish("my_topic", message_data)
        self.sns_adapter.sns_client.publish.assert_called_once_with(
            TargetArn="arn:aws:sns:us-east-1:123456789012:my_topic",
            Message='{"default": "{\\"key\\": \\"value\\"}"}',
            MessageStructure="json",
            MessageAttributes={"attr1": {"DataType": "String", "StringValue": "value1"}},
        )

    @patch.object(
        SNSAdapter, "_get_topic_arn", return_value="arn:aws:sns:us-east-1:123456789012:my_topic"
    )
    @patch("clever_events_library.events.adapters.sns_adapter.Session")
    def test_async_publish(self, mock_session, mock_get_topic_arn):
        message_data = {"message": {"key": "value"}, "message_attributes": {"attr1": "value1"}}
        mock_client = AsyncMock()
        mock_session.return_value.client.return_value.__aenter__.return_value = mock_client

        async def run_test():
            await self.sns_adapter.async_publish("my_topic", message_data)
            mock_client.publish.assert_called_once_with(
                TargetArn="arn:aws:sns:us-east-1:123456789012:my_topic",
                Message='{"default": "{\\"key\\": \\"value\\"}"}',
                MessageStructure="json",
                MessageAttributes={"attr1": {"DataType": "String", "StringValue": "value1"}},
            )

        asyncio.run(run_test())

    def test_sync_publish_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.sns_adapter.sync_publish("my_topic", {})

    def test_async_publish_raises_value_error(self):
        async def run_test():
            with self.assertRaises(ValueError):
                await self.sns_adapter.async_publish("my_topic", {})

        asyncio.run(run_test())

    @patch.object(
        SNSAdapter, "_get_topic_arn", return_value="arn:aws:sns:us-east-1:123456789012:my_topic"
    )
    def test_sync_publish_with_additional_params(self, mock_get_topic_arn):
        message_data = {"message": {"key": "value"}, "message_attributes": {"attr1": "value1"}}
        self.sns_adapter.sns_client.publish = MagicMock()
        additional_params = {"MessageGroupId": "test"}
        self.sns_adapter.sync_publish("my_topic", message_data, additional_params)
        self.sns_adapter.sns_client.publish.assert_called_once_with(
            TargetArn="arn:aws:sns:us-east-1:123456789012:my_topic",
            Message='{"default": "{\\"key\\": \\"value\\"}"}',
            MessageStructure="json",
            MessageAttributes={"attr1": {"DataType": "String", "StringValue": "value1"}},
            **additional_params
        )
