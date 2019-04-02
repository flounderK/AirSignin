import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client import file, client, tools
import google

import google_auth_oauthlib.flow


def get_sheet(creds, sheet_id):
    """Uses the google sheets api to pull down the full sheet"""
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    rows = list()

    data_range = "Sheet1!A{:d}:D"
    row_count = 2  # start at row 2 because of column headers
    end_found = False
    while not end_found:
        result = sheet.values().get(spreadsheetId=sheet_id, range=data_range.format(row_count)).execute()
        values = result.get("values", [])
        if len(values) == 0:
            end_found = True
        else:
            rows.append(tuple(values[0]))
        row_count += 1
    return rows


def make_creds():
    """Need to automate this"""
    # https://developers.google.com/sheets/api/quickstart/python
    scopes = "https://www.googleapis.com/auth/spreadsheets"
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scopes)
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes)
    creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


def main():
    sheet_id = None
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if os.path.exists("sheet_id"):
        with open("sheet_id", "r") as f:
            # re.search("(?<=/)([^/]+)(?=/edit#gid=0)", addr)[0]
            sheet_id = f.readline()

    sheet = get_sheet(creds, sheet_id)
    # Remove duplicate entries
    sheet = list(set(sheet))


