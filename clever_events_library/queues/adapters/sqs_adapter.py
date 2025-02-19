import boto3
import json
from . import QueueBaseAdapter


class SQSAdapter(QueueBaseAdapter):
    def __init__(self, client_config):
        self._validate_client_config(client_config)
        self.aws_region = client_config['aws_region']
        self.aws_account_id = client_config['aws_account_id']
        self.aws_key = client_config['aws_key']
        self.aws_secret = client_config['aws_secret']
        self.await_time = client_config.get('await_time', 20)
        self._sqs_client = None

    @property
    def sqs_client(self):
        if not self._sqs_client:
            self._sqs_client = boto3.client(
                "sqs",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret,
            )
        return self._sqs_client

    def _validate_client_config(self, client_config):
        required_keys = ['aws_region', 'aws_key', 'aws_secret', 'aws_account_id']
        for key in required_keys:
            if key not in client_config:
                raise ValueError(f'{key} is required in client_config')

    def fetch_messages(self, queue_name, max_number_of_messages=1):

        response = self.sqs_client.receive_message(
            QueueUrl=self._get_queue_url(queue_name=queue_name),
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=max_number_of_messages,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=self.await_time
        )

        messages = []
        if 'Messages' in response:
            for msg in response['Messages']:
                message_id = msg['MessageId']
                message_receipt_handle = msg['ReceiptHandle']
                message_body = json.loads(msg['Body'])
                message_attributes = message_body['MessageAttributes'] if 'MessageAttributes' in message_body else {}
                message_data = json.loads(message_body['Message'])
                messages.append({
                    'message_id': message_id,
                    'message_receipt_handle': message_receipt_handle,
                    'message_data': message_data,
                    'message_attributes': message_attributes
                })

        return messages

    def delete_message(self, queue_name, message_id):
        return self.sqs_client.delete_message(
            QueueUrl=self._get_queue_url(queue_name=queue_name),
            ReceiptHandle=message_id
        )

    def _get_queue_url(self, queue_name):
        return "https://sqs.{}.amazonaws.com/{}/{}".format(
            self.aws_region, self.aws_account_id, queue_name
        )
