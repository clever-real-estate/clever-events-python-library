import json

import boto3

from . import QueueBaseAdapter
from collections.abc import Iterator


class SQSAdapter(QueueBaseAdapter):
    def __init__(self, client_config: dict):
        """
        Initialize SQSAdapter with client_config

        Args:
            client_config (dict): This dict should contain the following
                keys:
                - aws_region: AWS region name
                - aws_account_id: AWS account id
                - aws_key: AWS access key
                - aws_secret: AWS secret key
                - await_time: Time to wait for messages in the queue

        Returns:
            None
        """
        self._validate_client_config(client_config)
        self.aws_region = client_config["aws_region"]
        self.aws_account_id = client_config["aws_account_id"]
        self.aws_key = client_config["aws_key"]
        self.aws_secret = client_config["aws_secret"]
        self.await_time = client_config.get("await_time", 20)
        self._sqs_client = None

    @property
    def sqs_client(self) -> boto3.client:
        if not self._sqs_client:
            self._sqs_client = boto3.client(
                "sqs",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret,
            )
        return self._sqs_client

    def _validate_client_config(self, client_config: dict):
        required_keys = ["aws_region", "aws_key", "aws_secret", "aws_account_id"]
        for key in required_keys:
            if key not in client_config:
                raise ValueError(f"{key} is required in client_config")

    def fetch_messages(self, queue_name: str, max_number_of_messages: int = 1) -> Iterator[dict]:
        """
        Fetch messages from the queue

        Args:
            queue_name (str): The name of the queue
            max_number_of_messages (int, optional): Highest number of messages we want to fetch. Defaults to 1.

        Yields:
            Iterator[dict]: A generator that yields messages from the queue
        """
        response = self.sqs_client.receive_message(
            QueueUrl=self._get_queue_url(queue_name=queue_name),
            AttributeNames=["All"],
            MaxNumberOfMessages=max_number_of_messages,
            MessageAttributeNames=["All"],
            VisibilityTimeout=0,
            WaitTimeSeconds=self.await_time,
        )

        if "Messages" in response:
            for msg in response["Messages"]:
                message_id = msg["MessageId"]
                message_receipt_handle = msg["ReceiptHandle"]
                message_body = json.loads(msg["Body"])
                message_attributes = (
                    message_body["MessageAttributes"]
                    if "MessageAttributes" in message_body
                    else {}
                )
                message_data = json.loads(message_body["Message"])
                yield {
                    "message_id": message_id,
                    "message_receipt_handle": message_receipt_handle,
                    "message_data": message_data,
                    "message_attributes": message_attributes,
                }

    def delete_message(self, queue_name: str, message_id: str) -> dict:
        """
        Delete a message from the queue

        Args:
            queue_name (str): The name of the queue
            message_id (str): The id of the message we want to delete

        Returns:
            dict: A dict containing the response we got from the stack when performing deletion
        """
        return self.sqs_client.delete_message(
            QueueUrl=self._get_queue_url(queue_name=queue_name), ReceiptHandle=message_id
        )

    def _get_queue_url(self, queue_name: str) -> str:
        return "https://sqs.{}.amazonaws.com/{}/{}".format(
            self.aws_region, self.aws_account_id, queue_name
        )
