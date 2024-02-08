import requests
import boto3
from botocore.exceptions import ClientError
import customtkinter as ctk
from tkinter import simpledialog

#App client ID: 47gg6er06v94205krc1gm5bpaq
#user pool ID: us-east-2_F7ah5pLy1
#user pool arn: arn:aws:cognito-idp:us-east-2:381491913371:userpool/us-east-2_F7ah5pLy1

def prompt_for_mfa_code():
    """Display a dialog to prompt the user for their MFA code."""
    app = ctk.CTk()
    app.withdraw()  # Hide the main window

    mfa_code = simpledialog.askstring("MFA Verification", "Enter the MFA code received via SMS:",
                                      parent=app)
    app.destroy()
    return mfa_code

def prompt_for_new_password():
    """Display a customtkinter dialog to prompt the user for a new password."""
    app = ctk.CTk()
    app.withdraw()  # Hide the main window

    new_password = simpledialog.askstring("New Password Required", "Enter your new password:",
                                          parent=app, show='*')
    app.destroy()
    return new_password

def prompt_for_attribute(attribute_name):
    """Display a dialog to prompt the user for a specific attribute."""
    app = ctk.CTk()
    app.withdraw()  # Hide the main window

    attribute_value = simpledialog.askstring(f"Enter {attribute_name}", f"Please enter your {attribute_name.replace('_', ' ')}:",
                                             parent=app)
    app.destroy()
    return attribute_value

def authenticate_user(username, password):
    client = boto3.client('cognito-idp', region_name='us-east-2')
    CLIENTID = '5lsps85k8pmmoei74avaevt7b5'

    try:
        auth_response = client.initiate_auth(
            ClientId=CLIENTID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        while True:  # Loop to handle multiple challenges if necessary
            if auth_response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                print("New password required for user.")
                new_password = prompt_for_new_password()
                phone_number = prompt_for_attribute('phone_number')  # Assuming you have already modified this function

                auth_response = client.respond_to_auth_challenge(
                    ClientId=CLIENTID,
                    ChallengeName='NEW_PASSWORD_REQUIRED',
                    Session=auth_response['Session'],
                    ChallengeResponses={
                        'USERNAME': username,
                        'NEW_PASSWORD': new_password,
                        'userAttributes.phone_number': phone_number
                    }
                )
                print("Password updated successfully.")
            elif auth_response.get('ChallengeName') == 'SMS_MFA':
                print("MFA code required for user.")
                mfa_code = prompt_for_mfa_code()

                auth_response = client.respond_to_auth_challenge(
                    ClientId=CLIENTID,
                    ChallengeName='SMS_MFA',
                    Session=auth_response['Session'],
                    ChallengeResponses={
                        'USERNAME': username,
                        'SMS_MFA_CODE': mfa_code
                    }
                )
                print("MFA verification successful.")
                break  # Exit loop if MFA challenge is passed
            else:
                break  # Exit loop if no more challenges
            print("Password updated successfully.")

    except ClientError as e:
        print("Authentication failed:", e)
        return None
    print(auth_response)
    return auth_response
