import json

import boto3

from . import EventBaseAdapter


class SNSAdapter(EventBaseAdapter):
    def __init__(self, client_config: dict) -> None:
        """
        Initialize SNSAdapter with client_config

        Args:
            client_config (dict): This dict should contain the following keys:
                - aws_region: AWS region name
                - aws_account_id: AWS account id
                - aws_key: AWS access key
                - aws_secret: AWS secret key

        Returns:
            None
        """
        self._validate_client_config(client_config)
        self.aws_region = client_config["aws_region"]
        self.aws_account_id = client_config["aws_account_id"]
        self.aws_key = client_config["aws_key"]
        self.aws_secret = client_config["aws_secret"]
        self._sns_client = None

    def _validate_client_config(self, client_config: dict) -> None:
        required_keys = ["aws_region", "aws_key", "aws_secret", "aws_account_id"]
        for key in required_keys:
            if key not in client_config:
                raise ValueError(f"{key} is required in client_config")

    @property
    def sns_client(self) -> boto3.client:
        if not self._sns_client:
            self._sns_client = boto3.client(
                "sns",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret,
            )
        return self._sns_client

    def publish(self, event_name: str, message_data: dict) -> None:
        """
        Publish a message to the SNS topic

        Args:
            event_name (str): The name of the SNS topic
            message_data (dict): A dict containing the message and message attributes. The message_data should have the following
                keys:
                - message: The message to be published
                - message_attributes: A dict containing the message attributes. It is optional.

        Raises:
            ValueError: If message is not present in message_data

        Returns:
            None
        """
        if "message" not in message_data:
            raise ValueError("message is required in message_data")
        message_attributes = message_data.get("message_attributes", {})
        self.sns_client.publish(
            TargetArn=self._get_topic_arn(topic_name=event_name),
            Message=json.dumps({"default": json.dumps(message_data["message"])}),
            MessageStructure="json",
            MessageAttributes=self._prepare_message_attributes(message_attributes),
        )

    def _get_topic_arn(self, topic_name: str) -> str:
        return "arn:aws:sns:{}:{}:{}".format(self.aws_region, self.aws_account_id, topic_name)

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
