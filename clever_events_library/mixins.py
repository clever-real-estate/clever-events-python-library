import os

from dotenv import load_dotenv

load_dotenv()


class AwsHelperMixin:
    def _get_aws_client_params(self, config_data: dict = {}) -> dict:
        """
        Get AWS client parameters from config_data or environment variables

        Args:
            config_data (dict, optional): A dict containing the following keys:
                - aws_region: AWS region name
                - aws_key: AWS access key
                - aws_secret: AWS secret key
                - aws_account_id: AWS account id
                Defaults to {}.

        Returns:
            Config: a dict containing the following keys:
                - aws_region: AWS region name
                - aws_key: AWS access key
                - aws_secret: AWS secret key
                - aws_account_id: AWS
        """

        aws_region = config_data.get("aws_region", os.environ.get("AWS_REGION"))
        aws_key = config_data.get("aws_key", os.environ.get("AWS_ACCESS_KEY_ID"))
        aws_secret = config_data.get("aws_secret", os.environ.get("AWS_SECRET_ACCESS_KEY"))
        aws_account_id = config_data.get("aws_account_id", os.environ.get("AWS_ACCOUNT_ID"))

        if not aws_region:
            raise ValueError("AWS_REGION is required")
        if not aws_key:
            raise ValueError("AWS_KEY is required")
        if not aws_secret:
            raise ValueError("AWS_SECRET is required")
        if not aws_account_id:
            raise ValueError("AWS_ACCOUNT_ID is required")

        return {
            "aws_key": aws_key,
            "aws_secret": aws_secret,
            "aws_region": aws_region,
            "aws_account_id": aws_account_id,
        }

    def _get_topic_arn(self, service: str, topic_name: str) -> str:
        return f"arn:aws:{service}:{self.aws_client_params['aws_region']}:{self.aws_client_params['aws_account_id']}:{topic_name}"
