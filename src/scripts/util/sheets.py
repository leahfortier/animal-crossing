import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import List, Dict

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Spreadsheet Link: https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>
SPREADSHEET_ID = '13d_LAJPlxMa_DubPTuirkIV4DERBMXbrWQsmSh8ReK4'

floor_item_tabs = ['Housewares', 'Miscellaneous']
item_tabs = [*floor_item_tabs, 'Wall-mounted']
ables_tabs = ['Tops', 'Bottoms', 'Dress-Up', 'Headwear', 'Accessories', 'Socks', 'Shoes']
clothing_tabs = [*ables_tabs, 'Bags', 'Umbrellas', 'Clothing Other']


def get_credentials():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is created
    # automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_sheet_data(spreadsheet_id: str, range_name: str) -> List[List[str]]:
    service = build('sheets', 'v4', credentials=get_credentials())

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    service.close()
    return values


# Stores all the rows of sheet
class Data:
    def __init__(self, spreadsheet_id: str, range_name: str):
        values = get_sheet_data(spreadsheet_id, range_name)
        full_schema = values[0]
        self.rows: List[List[str]] = values[1:]

        self.schema: Dict[str, int] = {}
        for i, val in enumerate(full_schema):
            self.schema[val] = i

    def has_key(self, key: str):
        return key in self.schema

    def get(self, key: str, row: List[str], remove_na: bool = False) -> str:
        if not self.has_key(key):
            print("Key '" + key + "' not in schema.")
            return ""

        value: str = row[self.schema.get(key)]
        if remove_na and value == "NA":
            value = ''

        return value

    def get_bool(self, key: str, row: List[str]) -> bool:
        value: str = self.get(key, row)
        assert value in ["Yes", "No"]
        return value == "Yes"


    def get_if(self, key: str, row: List[str], remove_na: bool = False) -> str:
        if self.has_key(key):
            return self.get(key, row, remove_na)
        else:
            return ''

    # Automatically sets the condition to whether or not the key exists
    def get_bool_if(self, key: str, row: List[str]) -> bool:
        if self.has_key(key):
            return self.get_bool(key, row)
        else:
            return False


def read_item_sheet(tab_name: str) -> Data:
    return Data(SPREADSHEET_ID, tab_name)
