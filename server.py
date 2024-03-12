import boto3
import datetime
import json

regionName = 'us-east-2'
identityPoolId = 'us-east-2:74dc5245-fd89-4280-9a4e-3a6a5a5d9d07'
cognitoIdentityProvider = 'cognito-idp.us-east-2.amazonaws.com/us-east-2_ZKhJrBN4H'
idToken = ''




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
    try:
        auth_response = q.get(timeout=10)  # Adjust timeout as needed
        print(f"Authentication response received: {auth_response}")
        # Process authentication response as needed
        ...
    except q.Empty:
        print("No authentication response received within timeout.")
        return  # or continue depending on your use case
    authResult = auth_response['AuthenticationResult']
    idToken = authResult['IdToken']
    print("ID Token: " + idToken)

    # get temporary access token and secret access token
    client = boto3.client('cognito-identity', region_name=regionName)

    # Get ID for the authenticated user from Cognito Identity Pool
    response = client.get_id(
        IdentityPoolId=identityPoolId,
        Logins={
            cognitoIdentityProvider: idToken
        }
    )

    identity_id = response['IdentityId']

    # Get credentials for the authenticated user
    creds_response = client.get_credentials_for_identity(
        IdentityId=identity_id,
        Logins={
            cognitoIdentityProvider: idToken
        }
    )

    # Extract the credentials
    credentials = creds_response['Credentials']

    # Use these credentials to access AWS services
    accessKeyID = credentials['AccessKeyId']
    secretAccessKey = credentials['SecretKey']
    sessionToken = credentials['SessionToken']

    print("Temporary Access Key ID: " + accessKeyID +
          "\nSecret Acces Key ID: " + secretAccessKey +
          "\nSession Token: " + sessionToken)


    # Create an SQS client
    sqs = boto3.client('sqs',
                       region_name=regionName,
                       aws_access_key_id=accessKeyID,
                       aws_secret_access_key=secretAccessKey,
                       aws_session_token=credentials['SessionToken'],
                       )

    def read_messages():
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,  # adjust this number as needed
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
