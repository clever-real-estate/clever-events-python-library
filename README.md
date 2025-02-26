# clever-events-python-library

The `clever-events-python-library` is a Python library designed to facilitate the publishing and management of events and messages using AWS services such as SNS (Simple Notification Service) and SQS (Simple Queue Service). This library provides a simple and efficient way to publish events both synchronously and asynchronously, as well as to fetch and delete messages from queues. It abstracts the complexities of interacting with AWS services, allowing developers to focus on building their applications without worrying about the underlying infrastructure.

## Usage Examples

### SNSAdapter with EventPublisher

#### Synchronous Publishing

```python
from clever_events_library.events.adapters import SNSAdapter
from clever_events_library.events.event_publisher import EventPublisher

sns_adapter = SNSAdapter({
    'aws_region': 'us-east-1',
    'aws_key': 'AWS_KEY',
    'aws_secret': 'AWS_SECRET',
    'aws_account_id': 'AWS_ACCOUNT_ID',
})

EventPublisher(event_adapter=sns_adapter).sync_publish(
    event_name='test_sns_topic',
    message_data={
        'message': {'test': 'TEST message'},
        'message_attributes': {
            'test1': 'test attributes 1',
        }
    }
)
```

#### Asynchronous Publishing

```python
from clever_events_library.events.adapters import SNSAdapter
from clever_events_library.events.event_publisher import EventPublisher
import asyncio

sns_adapter = SNSAdapter({
    'aws_region': 'us-east-1',
    'aws_key': 'AWS_KEY',
    'aws_secret': 'AWS_SECRET',
    'aws_account_id': 'AWS_ACCOUNT_ID',
})

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

event_publisher = EventPublisher(event_adapter=sns_adapter)
loop.run_until_complete(event_publisher.async_publish(
    event_name='test_sns_topic',
    message_data={
        'message': {'test': "TEST message"},
        'message_attributes': {
            'test': 'test attributes',
        }
    }
))
```

### SQSAdapter with QueueManager

#### Fetching and Deleting Messages

```python
from clever_events_library.queues.adapters import SQSAdapter
from clever_events_library.queues.queue_manager import QueueManager

sqs_adapter = SQSAdapter(
    {
        'aws_region': 'us-east-1',
        'aws_key': 'AWS_KEY',
        'aws_secret': 'AWS_SECRET',
        'aws_account_id': 'AWS_ACCOUNT_ID',
    }
)

sqs_adapter.set_await_time(20)

queue_manager = QueueManager(queue_adapter=sqs_adapter)
messages = queue_manager.fetch_messages(queue_name="noelias_test_queue", max_number_of_messages=10)

for message in messages:
    queue_manager.delete_message(queue_name="noelias_test_queue", message_id=message['message_receipt_handle'])
```

### AWS variables set up

AWS variables like region, account id and credentials can be configured as shown in examples above or can be set up in an environment (.env) file as follows:

```
AWS_REGION=AWS_REGION
AWS_ACCESS_KEY_ID=AWS_KEY
AWS_SECRET_ACCESS_KEY=AWS_SECRET
AWS_ACCOUNT_ID=AWS_ACCOUNT_ID
```

When those variables are added to .env file, it's not needed to explicitly include them in the adapter initialization.

So, the following code:

```
sqs_adapter = SQSAdapter(
    {
        'aws_region': 'us-east-1',
        'aws_key': 'AWS_KEY',
        'aws_secret': 'AWS_SECRET',
        'aws_account_id': 'AWS_ACCOUNT_ID',
    }
)
```

can be replaced with:

```
sqs_adapter = SQSAdapter()
```

Same applies to SNSAdapter.
