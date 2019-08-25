import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/drive.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gcp_credentials.json", scope)
client = gspread.authorize(creds)

# WARNING: This finds a sheet by name, if the sheet name changes, this will go boom
sheet = client.open("Hack Oregon 2019 Team Roster").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(json.dumps(list_of_hashes))
