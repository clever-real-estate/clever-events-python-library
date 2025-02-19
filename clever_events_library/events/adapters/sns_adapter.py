import json

import boto3

from . import EventBaseAdapter


class SNSAdapter(EventBaseAdapter):
    def __init__(self, client_config):
        self._validate_client_config(client_config)
        self.aws_region = client_config["aws_region"]
        self.aws_account_id = client_config["aws_account_id"]
        self.aws_key = client_config["aws_key"]
        self.aws_secret = client_config["aws_secret"]
        self._sns_client = None

    def _validate_client_config(self, client_config):
        required_keys = ["aws_region", "aws_key", "aws_secret", "aws_account_id"]
        for key in required_keys:
            if key not in client_config:
                raise ValueError(f"{key} is required in client_config")

    @property
    def sns_client(self):
        if not self._sns_client:
            self._sns_client = boto3.client(
                "sns",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret,
            )
        return self._sns_client

    def publish(self, event_name, message_data):
        if "message" not in message_data:
            raise ValueError("message is required in message_data")
        message_attributes = message_data.get("message_attributes", {})
        self.sns_client.publish(
            TargetArn=self._get_topic_arn(topic_name=event_name),
            Message=json.dumps({"default": json.dumps(message_data["message"])}),
            MessageStructure="json",
            MessageAttributes=self._prepare_message_attributes(message_attributes),
        )

    def _get_topic_arn(self, topic_name):
        return "arn:aws:sns:{}:{}:{}".format(self.aws_region, self.aws_account_id, topic_name)

    def _prepare_message_attributes(self, attributes):
        message_attributes = {}
        for key, value in attributes.items():
            value_key = "StringValue"
            value = str(value)
            message_attributes[key] = {
                "DataType": "String",
                value_key: value,
            }
        return message_attributes
