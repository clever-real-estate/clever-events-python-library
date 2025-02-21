# clever-events-python-library

Usage example for publishing events:

```
from clever_events_library.events.adapters import SNSAdapter
from clever_events_library.events.event_publisher import EventPublisher

sns_adapter = SNSAdapter({
    'aws_region': 'us-east-1',
    'aws_key': 'AWS_KEY',
    'aws_secret': 'AWS_SECRET',
    'aws_account_id': 'AWS_ACCOUNT_ID',
})

EventPublisher(event_adapter=sns_adapter).publish(
    event_name='noelias_test_std',
    message_data={
        'message': {'test': 'TEST message'},
        'message_attributes': {
            'test1': 'test attributes 1',
        }
    }
)
```

Usage example for fetching and deleting messages:

```
from clever_events_library.queues.adapters import SQSAdapter
from clever_events_library.queues.queue_manager import QueueManager


sqs_adapter = SQSAdapter(
    {
        'aws_region': 'us-east-1',
        'aws_key': 'AWS_KEY',
        'aws_secret': 'AWS_SECRET',
        'aws_account_id': 'AWS_ACCOUNT_ID',
        'await_time': 20
    }
)

queue_manager = QueueManager(queue_adapter=sqs_adapter)
messages = queue_manager.fetch_messages(queue_name="noelias_test_queue", max_number_of_messages=10)

for message in messages:
    queue_manager.delete_message(queue_name="noelias_test_queue", message_id=message['message_receipt_handle'])
```
