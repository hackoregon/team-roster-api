import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


# Lower case key names and trim white space
def normalize(record):
    return dict((k.lower().strip(), v.strip()) for k, v in record.items())


def get_roster():
    scope = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "gcp_credentials.json", scope
    )
    client = gspread.authorize(creds)

    # WARNING: This finds a sheet by name, if the sheet name changes, this will go boom
    sheet = client.open("Hack Oregon 2019 Team Roster").sheet1

    rows = sheet.get_all_records()
    rows = [normalize(x) for x in rows]

    res = {"data": rows}
    return res


# When running locally
if __name__ == "__main__":
    print(json.dumps(get_roster()))

