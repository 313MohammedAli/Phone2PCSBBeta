import boto3
import datetime
import json


# Create an SQS client
sqs = boto3.client('sqs',
                   region_name='us-east-2',
                   aws_access_key_id='AKIAVRUVQUKNSG2LPP66',
                   aws_secret_access_key='HZv8mmuLSgs7tDYh9vZSdbTo2oPcr/Wizvk808nA'
                   )

# Specify your queue URL
queue_url = 'https://sqs.us-east-2.amazonaws.com/381491913371/demoQueue'

# Extract button code from json response
# Pass the string from the body of the message and return string
def extractCode(message):
    # convert string to json
    body = json.loads(message)
    # Extract the value of Message key
    msg = body['Message']
    # Convert value of Message into json
    msg1 = json.loads(msg)
    # Extract the value of body key
    msg2 = msg1['body']
    # Convert the value of body to json
    msg3 = json.loads(msg2)
    # Extract value of code key
    msg4 = msg3['code']
    # return as a string
    return msg4



def main(q):
    def read_messages():
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberO1fMessages=10,  # adjust this number as needed
            WaitTimeSeconds=5  # long polling, up to 20 seconds
        )

        messages = response.get('Messages', [])
        if not messages:
            print(f"No messages received at {datetime.datetime.now()}")
            return

        for message in messages:
            # extract code from json message
            code = extractCode(message['Body'])

            print("Message ID:", message['MessageId'])
            print("Message Body:", code)
            print("Time: ", datetime.datetime.now())
            q.put(code)
            print(f"Succesfully put code {code} into queue")

            # Delete received message from queue
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

    while True:
        read_messages()
