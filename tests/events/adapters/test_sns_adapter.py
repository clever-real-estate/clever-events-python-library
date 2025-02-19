import unittest
from unittest.mock import patch, MagicMock
from clever_events_library.events.adapters.sns_adapter import SNSAdapter


class TestSNSAdapter(unittest.TestCase):

    def setUp(self):
        self.client_config = {
            'aws_region': 'us-east-1',
            'aws_account_id': '123456789012',
            'aws_key': 'fake_key',
            'aws_secret': 'fake_secret'
        }
        self.sns_adapter = SNSAdapter(self.client_config)

    def test_validate_client_config(self):
        with self.assertRaises(ValueError):
            invalid_config = {
                'aws_region': 'us-east-1',
                'aws_key': 'fake_key',
                'aws_secret': 'fake_secret'
            }
            SNSAdapter(invalid_config)

    @patch('boto3.client')
    def test_sns_client_initialization(self, mock_boto_client):
        mock_boto_client.return_value = MagicMock()
        sns_client = self.sns_adapter.sns_client
        self.assertIsNotNone(sns_client)
        mock_boto_client.assert_called_once_with(
            "sns",
            region_name=self.client_config['aws_region'],
            aws_access_key_id=self.client_config['aws_key'],
            aws_secret_access_key=self.client_config['aws_secret']
        )

    @patch.object(SNSAdapter, 'sns_client', new_callable=MagicMock)
    def test_publish(self, mock_sns_client):
        mock_sns_client.publish = MagicMock()
        event_name = 'test_event'
        message_data = {
            'message': {'key': 'value'},
            'message_attributes': {'attr1': 'value1'}
        }
        self.sns_adapter.publish(event_name, message_data)
        mock_sns_client.publish.assert_called_once()

    def test_publish_missing_message(self):
        with self.assertRaises(ValueError):
            self.sns_adapter.publish('test_event', {})

    def test_get_topic_arn(self):
        topic_name = 'test_topic'
        expected_arn = "arn:aws:sns:us-east-1:123456789012:test_topic"
        self.assertEqual(self.sns_adapter._get_topic_arn(topic_name), expected_arn)

    def test_prepare_message_attributes(self):
        attributes = {'attr1': 'value1'}
        expected_attributes = {
            'attr1': {
                'DataType': 'String',
                'StringValue': 'value1'
            }
        }
        self.assertEqual(self.sns_adapter._prepare_message_attributes(attributes), expected_attributes)
