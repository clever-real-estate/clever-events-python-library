import json

import boto3
from aioboto3.session import Session

from ...mixins import AwsHelperMixin
from . import EventBaseAdapter


class SNSAdapter(AwsHelperMixin, EventBaseAdapter):
    def __init__(self, client_config: dict = {}) -> None:
        """
        Initialize SNSAdapter with client_config

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
        self._sns_client = None

    @property
    def sns_client(self) -> boto3.client:
        if not self._sns_client:
            self._sns_client = boto3.client(
                "sns",
                region_name=self.aws_client_params["aws_region"],
                aws_access_key_id=self.aws_client_params["aws_key"],
                aws_secret_access_key=self.aws_client_params["aws_secret"],
            )
        return self._sns_client

    def sync_publish(self, event_name: str, message_data: dict, additional_params: dict = {}) -> None:
        """
        Synchronously publish a message to the SNS topic

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message and message attributes. The message_data should have the following
                keys:
                - message: The message to be published
                - message_attributes: A dict containing the message attributes. It is optional.
            additional_params: A dict containing additional parameters. It is optional.

        Raises:
            ValueError: If message is not present in message_data

        Returns:
            None
        """
        if "message" not in message_data:
            raise ValueError("message is required in message_data")
        message_attributes = message_data.get("message_attributes", {})
        self.sns_client.publish(
            TargetArn=self._get_topic_arn(service="sns", topic_name=event_name),
            Message=json.dumps({"default": json.dumps(message_data["message"])}),
            MessageStructure="json",
            MessageAttributes=self._prepare_message_attributes(message_attributes),
            **additional_params
        )

    async def async_publish(self, event_name: str, message_data: dict, additional_params: dict = {}) -> None:
        """
        Asynchronously publish a message to the SNS topic

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message and message attributes. The message_data should have the following
                keys:
                - message: The message to be published
                - message_attributes: A dict containing the message attributes. It is optional.
            additional_params (dict): A dict containing additional parameters. It is optional.

        Raises:
            ValueError: If message is not present in message_data

        Returns:
            None
        """
        if "message" not in message_data:
            raise ValueError("message is required in message_data")
        message_attributes = message_data.get("message_attributes", {})

        session = Session()
        async with session.client(
            "sns",
            region_name=self.aws_client_params["aws_region"],
            aws_access_key_id=self.aws_client_params["aws_key"],
            aws_secret_access_key=self.aws_client_params["aws_secret"],
        ) as client:
            await client.publish(
                TargetArn=self._get_topic_arn(service="sns", topic_name=event_name),
                Message=json.dumps({"default": json.dumps(message_data["message"])}),
                MessageStructure="json",
                MessageAttributes=self._prepare_message_attributes(message_attributes),
                **additional_params
            )

    def _prepare_message_attributes(self, attributes: dict) -> dict:
        message_attributes = {}
        for key, value in attributes.items():
            value_key = "StringValue"
            value = str(value)
            message_attributes[key] = {
                "DataType": "String",
                value_key: value,
            }
        return message_attributes
