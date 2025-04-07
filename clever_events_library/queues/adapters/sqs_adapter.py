import json
from collections.abc import Iterator

import boto3

from ...mixins import AwsHelperMixin
from . import QueueBaseAdapter


class SQSAdapter(AwsHelperMixin, QueueBaseAdapter):
    def __init__(self, client_config: dict = {}) -> None:
        """
        Initialize SQSAdapter with client_config

        Args:
            client_config (dict): This dict should contain the following
                keys:
                - aws_region: AWS region name
                - aws_account_id: AWS account id
                - aws_key: AWS access key
                - aws_secret: AWS secret key
            If not provided, values will be fetched from environment variables.
            Defaults to {}.

        Returns:
            None
        """
        self.aws_client_params = self._get_aws_client_params(client_config)
        self._sqs_client = None
        self._await_time = 0

    def set_await_time(self, await_time: int) -> None:
        """
        Set the time to wait for messages

        Args:
            await_time (int): The time to wait for messages

        Returns:
            None
        """
        self._await_time = await_time

    @property
    def sqs_client(self) -> boto3.client:
        if not self._sqs_client:
            self._sqs_client = boto3.client(
                "sqs",
                region_name=self.aws_client_params["aws_region"],
                aws_access_key_id=self.aws_client_params["aws_key"],
                aws_secret_access_key=self.aws_client_params["aws_secret"],
            )
        return self._sqs_client

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
            WaitTimeSeconds=self._await_time,
        )

        if "Messages" in response:
            for msg in response["Messages"]:
                message_id = msg["MessageId"]
                message_receipt_handle = msg["ReceiptHandle"]
                message_body = json.loads(msg["Body"])
                message_attributes = (
                    msg["MessageAttributes"]
                    if "MessageAttributes" in msg
                    else {}
                )
                yield {
                    "message_id": message_id,
                    "message_receipt_handle": message_receipt_handle,
                    "message_data": message_body,
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
            self.aws_client_params["aws_region"],
            self.aws_client_params["aws_account_id"],
            queue_name,
        )
