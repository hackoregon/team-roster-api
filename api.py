import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import boto3
import os

AWS_PROFILE = os.environ.get("AWS_PROFILE")
aws_session = boto3.session.Session(profile_name=AWS_PROFILE)
aws = aws_session.client("ssm")

# Lower case key names and trim white space
def normalize(record):
    return dict((k.lower().strip(), v.strip()) for k, v in record.items())


def get_roster():
    scope = ["https://www.googleapis.com/auth/drive.readonly"]
    ssm_response = aws.get_parameter(
        Name="/production/team-roster/gcp-credentials", WithDecryption=True
    )

    creds_json = json.loads(ssm_response["Parameter"]["Value"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scopes=scope)
    client = gspread.authorize(creds)

    # WARNING: This finds a sheet by name, if the sheet name changes, this will go boom
    sheet = client.open("Hack Oregon 2019 Team Roster").sheet1

    rows = sheet.get_all_records()
    rows = [normalize(x) for x in rows]
    return rows


def lambda_handler(event, context):
    return {"statusCode": 200, "data": get_roster()}


# When running locally
if __name__ == "__main__":
    print(json.dumps(lambda_handler()))

